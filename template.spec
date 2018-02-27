%global pkgname {{ pypi['info']['name'] }}

Name:           python3-%{pkgname}
Version:        {{ pypi['info']['version'] }}
Release:        1%{?dist}
Summary:        Summary

License:        License
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
BuildRequires:  python3dist({{ package|lower }})
{% endfor %}

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
%{python3_sitearch}/*.so

%changelog
* Tue Feb 27 2018 Lumír Balhar <lbalhar@redhat.com> - 0.26.3-1
- Some changelog entry
