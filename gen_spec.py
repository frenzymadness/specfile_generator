import sys
from subprocess import call, check_output
from tempfile import TemporaryDirectory

import os
import re
import requests
from jinja2 import Template


def get_installed_files(packagename):
    with TemporaryDirectory() as tempvenv:
        call(['python3', '-m', 'venv', tempvenv])
        venv_pip = [tempvenv + '/bin/python', '-m', 'pip']
        call(venv_pip + ['install', packagename])
        result = check_output(venv_pip + ['show', '-f', packagename])
    files = [str(line.strip(), 'utf-8') for line in result.split(b'\n')
             if line.startswith(b'  ')]
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


def get_license(packagename):
    with TemporaryDirectory() as tempvenv:
        call(['python3', '-m', 'venv', tempvenv])
        venv_pip = [tempvenv + '/bin/python', '-m', 'pip']
        call(venv_pip + ['install', packagename])
        result = check_output(venv_pip + ['show', '-f', packagename])
        result = result.decode()

        for line in result.split('\n'):
            found_at = line.find('Location: ')
            if found_at == 0:
                path = line[len('Location: '):] + '/'

                for file_dir in os.listdir(path):
                    if file_dir.startswith(packagename) and (file_dir.find('dist-info') != -1):
                        path_to_license = path + file_dir + '/LICENSE'
                        return os.path.relpath(path_to_license, start=path)

print(get_license('requests'))
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

    all_package_files = get_installed_files(packagename)
    files = filter_files(packagename, all_package_files)

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
