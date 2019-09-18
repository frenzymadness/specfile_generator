%global pkgname {{ pypi['info']['name'] }}

Name:           python-%{pkgname}
Version:        {{ pypi['info']['version'] }}
Release:        1%{?dist}
Summary:        {{ pypi['info']['summary']}}
# todo: check if the license match with rpm list of licences
License:        {{ pypi['info']['license']}}
URL:            {{ (pypi['info']['home_page'] or pypi['info']['project_url']) }}
Source0:        {{ (pypi['info']['download_url'] or source_url) }}

BuildArch:      noarch
BuildRequires:  pyproject-rpm-macros

%description
{{pypi['info']['description']}}

%package -n python3-%{pkgname}
# Auto Python dependency
BuildRequires:  python3-devel
# Automatic runtime dependency generator
%?python_enable_dependency_generator

Summary: %{summary}
%description -n python3-%{pkgname}
{{pypi['info']['description']}}

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
{% for file in files %}{{ file }}
{% endfor %}

# todo: missing %license (get from manifest.in maybe)
# todo: missing %doc (not that important)

%changelog
* Tue Feb 27 2018 Lumir Balhar <lbalhar@redhat.com> - 0.26.3-1
- Some changelog entry
