import requests
import sys

from jinja2 import Template
import mock
import setuptools
import toml


def get_pypi_metadata(packagename):
    URL = 'http://pypi.python.org/pypi/{}/json'.format(packagename)
    response = requests.get(URL)
    return response.json()


# def get_setup_metadata(packagename, version):
#     sys.path.insert(0, './{}-{}/'.format(packagename, version))

#     with mock.patch.object(setuptools, 'setup') as mock_setup:
#         import setup  # noqa

#     args, kwargs = mock_setup.call_args
#     extracted = {}
#     for kwarg in 'license', 'install_requires':
#         extracted[kwarg] = kwargs.get(kwarg, None)

#     return extracted


def get_pyproject_toml_metadata(packagename, version):
    pyproject_file_name = '{}-{}/pyproject.toml'.format(packagename, version)
    toml_data = toml.load(pyproject_file_name)
    return toml_data


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

    toml_data = get_pyproject_toml_metadata(packagename, version)

    python_build_requires = toml_data['build-system']['requires']
    rpm_build_requires = toml_data['build-system']['requires-rpm']

    result = template.render(pypi=pypi_data,
                             source_url=source_url,
                             python_build_requires=python_build_requires,
                             rpm_build_requires=rpm_build_requires)

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
