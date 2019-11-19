# specfile_generator
This project is about generating specfile through metadata we can get from pypi api,
or later with source distribution.

The problems of handling build dependencies or
running tests etc. will handle [pyproject-rpm-macros](https://src.fedoraproject.org/rpms/pyproject-rpm-macros)

## Dependencies


In order to run the specfile generator, you will need this dependencies installed

* Python >= 3.5
* Python modules:
    * jinja2
    * requests

In Fedora, all dependencies can be installed via dnf: `sudo dnf install python3-jinja2 python3-requests`. Or you can install dependencies via pip into virtual environment.


### Generate specfile

```
$ python3 gen_spec.py hypothesis
```

~~~~
$ cat hypothesis.spec

%global pkgname hypothesis

Name:           python-%{pkgname}
Version:        4.42.3
Release:        1%{?dist}
Summary:        A library for property based testing
# todo: check if the license match with rpm list of licences
License:        MPL v2
URL:            https://pypi.org/project/hypothesis/
Source0:        https://files.pythonhosted.org/packages/db/43/eda2a8a6d77a81cf211bb99fb02e3b5c65f993024b4e738f7ffc593f9777/hypothesis-4.42.3.tar.gz

BuildArch:      noarch
BuildRequires:  pyproject-rpm-macros

%description
==========
Hypothesis
==========

Hypothesis is an advanced testing library for Python. It lets you write tests which
are parametrized by a source of examples, and then generates simple and comprehensible
examples that make your tests fail. This lets you find more bugs in your code with less
work.
...



%prep
%autosetup -n %{pkgname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install

# %%check
# %%tox

%files -n python3-%{pkgname}
%{python3_sitelib}/hypothesis-4.42.3.dist-info/
%{python3_sitelib}/hypothesis/


# todo: missing %license (get from manifest.in maybe)
# todo: missing %doc (not that important)

%changelog
* Tue Feb 27 2018 Lumír Balhar <lbalhar@redhat.com> - 0.26.3-1
- Some changelog entry
~~~~

### Build source and binary RPM
[rpm guide](https://fedoraproject.org/wiki/How_to_create_a_GNU_Hello_RPM_package)  
[simpler Fedora specific guide](https://docs.fedoraproject.org/en-US/quick-docs/creating-rpm-packages/)

### Things to handle ###
<ul>
    <li>rpmlint isn't very happy about our generated specfiles
    <ul>
        <li>description line is too long</li>
        <li>name of package
            <ul>
                <li>name of specfile isn't same as rpm, figure out if the package should be named $name_of_project.spec or 
                python-$name_of_project.spec.</li>
                <li>normalize text to meet Fedora guidelines e.g. python-Flask -> python-flask
            </ul>
        </li>
        <li>in preamble `License:` shortcut of License doesn't need to be same
        as rpm expect</li>
        <li>etc.</li>
    </ul>
    </li>
    <li>check in sdist for tox.ini and use %tox macro for running tests</li>
    <li>test script how big proportion of packages can build especially for C extensions</li>
    <li>move handling of generating file section to rpm macro</li>
</ul>