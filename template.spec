%global pkgname {{ pypi['info']['name'] }}

Name:           python-%{pkgname}
Version:        {{ pypi['info']['version'] }}
Release:        1%{?dist}
Summary:        Python bindings for libgit2

License:        GPLv2 with linking exception
URL:            {{ pypi['info']['package_url'] }}
Source0:        {{ source_url }}

# Auto Python dependency
BuildRequires:  python3-devel

# Non-Python deps
{% for package in fedora_build_requires -%}
BuildRequires:  {{ package }}
{% endfor %}

# Python deps
{% for package in python_build_requires -%}
BuildRequires:  python3dist({{ package }})
{% endfor %}

Requires:       python3-cffi
Requires:       python3-six

%description
pygit2 is a set of Python bindings to the libgit2 library, which implements
the core of Git.


%prep
%autosetup -n %{pkgname}-%{version} -p1

# Remove failing create_from tests
# https://github.com/libgit2/pygit2/issues/748
# rm test/test_patch.py

%build
%py3_build


%install
%py3_install

# Correct the permissions.
find %{buildroot} -name '*.so' -exec chmod 755 {} ';'

%{__python3} setup.py test

%files
%doc README.rst TODO.txt
%license COPYING
%{python3_sitearch}/%{pkgname}-%{version}-py%{python3_version}.egg-info
%{python3_sitearch}/%{pkgname}
%{python3_sitearch}/_%{pkgname}.*.so

%changelog
* Tue Feb 27 2018 Lumír Balhar <lbalhar@redhat.com> - 0.26.3-1
- Some changelog entry
