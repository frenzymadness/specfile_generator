import atexit
import sys
from subprocess import call, check_output
from tempfile import TemporaryDirectory

import os
import re
import requests
from jinja2 import Template


def python3_macros():
    macros = {
    '%{python3_sitelib}': '',
    '%{python3_sitearch}': '',
    '%{_bindir}'
    '%{python3_version}': '',
    '%{python3_version_nodots}': ''}
    
    for key, value in macros.items():
        expanded = check_output(['rpm', '--eval', key])
        macros[key] = (expanded.decode()).strip()
    return macros
print(python3_macros())


def prepare_venv(packagename):
    tempvenv = TemporaryDirectory()
    atexit.register(tempvenv.cleanup)
    tempvenv = tempvenv.__enter__()
    call(['python3', '-m', 'venv', tempvenv])
    venv_pip = [tempvenv + '/bin/python', '-m', 'pip']
    call(venv_pip + ['install', packagename])
    return venv_pip, tempvenv


def get_installed_files(packagename, venv_pip, temp_dir):
    # todo: check how rpm behaves when having
    # f'{prefix}/../../../bin/something'
    result = check_output(venv_pip + ['show', '-f', packagename])
    result = (result.decode()).split('\n')
    for line in result:
        if line.startswith('Location:'):
            line = line[len('Location: '):]
            prefix =  '/' + line.replace(temp_dir, 'usr') + '/'
            break
    
    files = [prefix + line.strip() for line in result
             if line.startswith('  ')]
    return files


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


def generate_specfile(packagename):
    with open('template.spec') as template_file:
        template = Template(template_file.read())

    pypi_data = get_pypi_metadata(packagename)
    version = pypi_data['info']['version']
    release = pypi_data['releases'][version]
    for source in release:
        if source['python_version'] == 'source':
            source_url = source['url']
            break
    
    venv_pip, temp_dir = prepare_venv(packagename)

    all_package_files = get_installed_files(packagename, venv_pip, temp_dir)
    # files = filter_files(packagename, all_package_files)
    files = all_package_files
    result = template.render(pypi=pypi_data,
                             source_url=source_url,
                             files=files)

    with open('{}.spec'.format(packagename), 'w') as spec_file:
        spec_file.write(result)


def main():
    if len(sys.argv) < 2:
        print('Package name(s) not provided!')
        sys.exit(1)
    else:
        for packagename in sys.argv[1:]:
            generate_specfile(packagename)


if __name__ == '__main__':
    main()