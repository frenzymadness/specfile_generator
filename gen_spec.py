import argparse
import atexit
from datetime import date
import sys
from subprocess import call, check_output, CalledProcessError
from tempfile import TemporaryDirectory
import os

import requests
from jinja2 import Template

template_path = os.path.dirname(os.path.abspath(__file__)) + '/template.spec'


def get_installed_files(packagename, venv_pip, temp_dir):
    """return list of files looking like installed in system"""
    result = check_output(venv_pip + ['show', '-f', packagename])
    result = (result.decode()).split('\n')
    files = []

    for line in result:
        # this line contains path to venv directory
        if line.startswith('Location:'):
            line = line[len('Location: '):]
            prefix = '/' + line.replace(temp_dir, 'usr') + '/'
        if line.startswith(' '*2):
            path = os.path.abspath(prefix + line.strip())
            if os.path.isdir(path):
                path += "/"
            files.append(path)
    return files


def prepare_venv(packagename):
    tempdir = TemporaryDirectory()
    atexit.register(tempdir.cleanup)
    tempdir = tempdir.__enter__()
    call(['python3', '-m', 'venv', tempdir])
    venv_pip = [tempdir + '/bin/python', '-m', 'pip']
    call(venv_pip + ['install', packagename])
    return venv_pip, tempdir


def path_macros():
    macros = {
        '%{python3_sitelib}': '',
        '%{python3_sitearch}': '',
        '%{_bindir}': '',
        '%{python3_version}': '',
        '%{python3_version_nodots}': ''}

    for key in macros.keys():
        expanded = check_output(['rpm', '--eval', key])
        macros[key] = (expanded.decode()).strip() 
    return macros


def files_with_macros(files, macros):
    # files should be sorted
    files = '\n'.join(files)
    for macro, value in macros.items():
        files = files.replace(value, macro)
    return files.split('\n')


# shouldn't work when library contains multiple modules
def group_files(files):
    exclude_paths = []
    grouped_files = []
    for file in files:
        # Do not add files in exluded (already processed) folders
        if any(True for path in exclude_paths if file.startswith(path)):
            continue
        # Add folder as is
        if file.endswith("/"):
            grouped_files.append(file)
            continue
        # Special case for __pycache__ directories in root directories
        first, second, *rest = file.split("/")
        if first.startswith("%") and second == "__pycache__":
            grouped_files.append(f"{first}/{second}/*")
            continue
        # Add a whole folder instead of each file
        if rest:
            dirname = os.path.dirname(file)
            exclude_paths.append(dirname)
            grouped_files.append(dirname + "/")
            continue
        # Ad iff nothing else was added
        grouped_files.append(file)

    return grouped_files


def filter_files(packagename, files):
    files_list_final = []
    for file in files:
        # Do not include dist-info
        if '.dist-info/' in file:
            continue

        # Skip all files in package base folder (added automatically)
        if file.startswith(packagename + '/'):
            continue

        files_list_final.append('%{python3_sitearch}/' + file)

    return files_list_final


def get_pypi_metadata(packagename):
    URL = 'https://pypi.python.org/pypi/{}/json'.format(packagename)
    response = requests.get(URL)
    return response.json()


def changelog_head(email, name):
    """ :returns f'{date} {name} <{email}>'"""
    today = (date.today()).strftime('%a %b %d %Y')

    if email or name:
        return f'{today} {name} <{email}>'

    try:
        result = check_output(['rpmdev-packager'])
        result = result.decode().strip()
    except CalledProcessError:
        result = " <>"

    return f'{today} {result}'


def generate_specfile(packagename, version, debug, email, name):
    with open(template_path) as template_file:
        template = Template(template_file.read())

    pypi_data = get_pypi_metadata(packagename)
    version = (version or pypi_data['info']['version'])
    release = pypi_data['releases'][version]
    for source in release:
        if source['python_version'] == 'source':
            source_url = source['url']
            break

    venv_pip, temp_dir = prepare_venv(packagename)

    macros = path_macros()
    all_package_files = get_installed_files(packagename, venv_pip, temp_dir)
    files = files_with_macros(all_package_files, macros)
    files = group_files(files)
    if debug:
        files += ['#' + files for files in all_package_files]

    result = template.render(pypi=pypi_data,
                             source_url=source_url,
                             files=files,
                             version=version,
                             changelog_head=changelog_head(email, name))

    with open('{}.spec'.format(packagename), 'w') as spec_file:
        spec_file.write(result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('package', help='name of package stored in pypi')
    parser.add_argument('--version', help='version of package, default is the newest version')
    parser.add_argument('--debug', help='specfile will contain more information', action='store_true')
    parser.add_argument('--email', help='changelog will contain this email')
    parser.add_argument('--name', help='changelog will contain this name')
    args = parser.parse_args()
    generate_specfile(args.package, args.version, args.debug, args.email, args.name)


if __name__ == '__main__':
    main()
