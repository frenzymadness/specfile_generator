# specfile_generator

Proof of concept of generator for RPM specfiles from (enhanced) [pyproject.toml files (PEP 518)](https://www.python.org/dev/peps/pep-0518/). If this approach of rebuilding PyPI packages in RPM form will work, files in `pyproject_toml_files` may become a part of upstream projects or can be maintained as patches for upstream pyproject.toml files.

## Dependencies

In order to run the specfile generator, you will need this dependencies installed

* Python >= 3.5
* Python modules:
    * jinja2
    * toml
    * requests

In Fedora, all dependencies can be installed via dnf: `sudo dnf install python3-jinja2 python3-toml python3-requests`. Or you can install dependencies via pip into virtual environment.

## pyproject.toml files

Currently, only few `pyproject.toml` files are available so if you want to try rebuild package from PyPI to RPM, you have to create a new `pyproject.toml` named `<oypi_pkg_name>.toml` in `pyproject_toml_files`. `pyproject.toml` file can be derived from upstream version of this file.

In every `pyproject.toml` file, there have to be two lists of packages in `[build-system]` section.

* `requires` contains a list of python build dependencies (PyPI names)
* `requires-fedora` contains a list of RPM packages which will be transferred to `BuildRequires` in generated specfile.

## Example usage

Generator can generate RPM specfile from `template.spec` with information from PyPI and files in `pyproject_toml_files` folder.

### Generate specfile

```
$ python3 gen_spec.py pygit2
```

```
$ cat pygit2.spec

%global pkgname pygit2

Name:           python3-%{pkgname}
Version:        0.26.3
Release:        1%{?dist}
Summary:        Summary

License:        License
URL:            http://pypi.python.org/pypi/pygit2
Source0:        https://pypi.python.org/packages/29/78/c2d5c7b0394e99cf20c683927871e676ff796d69d8c2c322e0edabb6e9c6/pygit2-0.26.3.tar.gz

# Auto Python dependency
BuildRequires:  python3-devel

# Non-Python deps
BuildRequires:  libgit2-devel
BuildRequires:  openssl-devel


# Python deps
BuildRequires:  python3dist(cffi)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(six)


# Automatic runtime dependency generator
%?python_enable_dependency_generator

%description
...

%prep
%autosetup -n %{pkgname}-%{version}

%build
%py3_build

%install
%py3_install

# %check
# %{__python3} setup.py test

%files
%{python3_sitearch}/%{pkgname}-%{version}-py%{python3_version}.egg-info
%{python3_sitearch}/%{pkgname}

%{python3_sitearch}/_pygit2.cpython-36m-x86_64-linux-gnu.so


%changelog
* Tue Feb 27 2018 Lumír Balhar <lbalhar@redhat.com> - 0.26.3-1
- Some changelog entry
```

### Build source and binary RPM

```
$ rpmbuild -bs pygit2.spec
```

and

```
$ mock <source RPM path>/python3-pygit2-0.26.3-1.fc27.src.rpm
```
