%global pkgname {{ pypi['info']['name'] }}

# todo: This is not valid specfile
Name:           python-%{pkgname}
Version:        {{ pypi['info']['version'] }}
Release:        1%{?dist}
Summary:        {{ pypi['info']['summary']}}
# todo: check if the license match with rpm list of licences
License:        {{ pypi['info']['license']}}
URL:            {{ pypi['info']['Home-page'] }}
Source0:        {{ (pypi['info']['download_url'] or source_url) }}
%description
{{pypi['info']['description']}}

%package -n python3-%{pkgname}
# Auto Python dependency
BuildRequires:  python3-devel

# Automatic runtime dependency generator
%?python_enable_dependency_generator

%description
{{pypi['info']['description']}}

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
# todo: missing __pycache__
{% for file in files %}
{{ file }}
{% endfor %}

# todo: missing %license (get from manifest.in maybe)
# todo: missing %doc (not that important)

%changelog
* Tue Feb 27 2018 Lumír Balhar <lbalhar@redhat.com> - 0.26.3-1
- Some changelog entry
