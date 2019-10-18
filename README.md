# specfile_generator

Goal is automate making of specfiles of python packages on pypi for Fedora.

## Dependencies

In order to run the specfile generator, you will need this dependencies installed

* Python >= 3.5
* Python modules:
    * jinja2
    * requests

In Fedora, all dependencies can be installed via dnf: `sudo dnf install python3-jinja2 python3-requests`. Or you can install dependencies via pip into virtual environment.

## usage
~~~~
usage: gen_spec [-h] [--version VERSION] [--debug] package

positional arguments:
  package            name of package stored in pypi

optional arguments:
  -h, --help         show this help message and exit
  --version VERSION  version of package, default is the newest version
  --debug            specfile will contain more information,
                     for now it writes to spec list of all files gotten from virtual environment
                
~~~~

### Generate specfile

```
$ python3 gen_spec requests
```
~~~
$ cat requests.spec

%global pkgname requests

Name:           python-%{pkgname}
Version:        2.22.0
Release:        1%{?dist}
Summary:        Python HTTP for Humans.
# todo: check if the license match with rpm list of licences
License:        Apache 2.0
URL:            https://pypi.org/project/requests/
Source0:        https://files.pythonhosted.org/packages/01/62/ddcf76d1d19885e8579acb1b1df26a852b03472c0e46d2b959a714c90608/requests-2.22.0.tar.gz

BuildArch:      noarch
BuildRequires:  pyproject-rpm-macros

%description
Requests: HTTP for Humans™
==========================

[![image](https://img.shields.io/pypi/v/requests.svg)](https://pypi.org/project/requests/)
[![image](https://img.shields.io/pypi/l/requests.svg)](https://pypi.org/project/requests/)
[![image](https://img.shields.io/pypi/pyversions/requests.svg)](https://pypi.org/project/requests/)
[![codecov.io](https://codecov.io/github/requests/requests/coverage.svg?branch=master)](https://codecov.io/github/requests/requests)
[![image](https://img.shields.io/github/contributors/requests/requests.svg)](https://github.com/requests/requests/graphs/contributors)
[![image](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/kennethreitz)

Requests is the only *Non-GMO* HTTP library for Python, safe for human
consumption.

![image](https://farm5.staticflickr.com/4317/35198386374_1939af3de6_k_d.jpg)

Behold, the power of Requests:

``` {.sourceCode .python}
>>> import requests
>>> r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
>>> r.status_code
200
>>> r.headers['content-type']
'application/json; charset=utf8'
>>> r.encoding
'utf-8'
>>> r.text
u'{"type":"User"...'
>>> r.json()
{u'disk_usage': 368627, u'private_gists': 484, ...}
```

See [the similar code, sans Requests](https://gist.github.com/973705).

[![image](https://raw.githubusercontent.com/requests/requests/master/docs/_static/requests-logo-small.png)](http://docs.python-requests.org/)

Requests allows you to send *organic, grass-fed* HTTP/1.1 requests,
without the need for manual labor. There's no need to manually add query
strings to your URLs, or to form-encode your POST data. Keep-alive and
HTTP connection pooling are 100% automatic, thanks to
[urllib3](https://github.com/shazow/urllib3).

Besides, all the cool kids are doing it. Requests is one of the most
downloaded Python packages of all time, pulling in over 11,000,000
downloads every month. You don't want to be left out!

Feature Support
---------------

Requests is ready for today's web.

-   International Domains and URLs
-   Keep-Alive & Connection Pooling
-   Sessions with Cookie Persistence
-   Browser-style SSL Verification
-   Basic/Digest Authentication
-   Elegant Key/Value Cookies
-   Automatic Decompression
-   Automatic Content Decoding
-   Unicode Response Bodies
-   Multipart File Uploads
-   HTTP(S) Proxy Support
-   Connection Timeouts
-   Streaming Downloads
-   `.netrc` Support
-   Chunked Requests

Requests officially supports Python 2.7 & 3.4–3.7, and runs great on
PyPy.

Installation
------------

To install Requests, simply use [pipenv](http://pipenv.org/) (or pip, of
course):

``` {.sourceCode .bash}
$ pipenv install requests
✨🍰✨
```

Satisfaction guaranteed.

Documentation
-------------

Fantastic documentation is available at
<http://docs.python-requests.org/>, for a limited time only.

How to Contribute
-----------------

1.  Become more familiar with the project by reading our [Contributor's Guide](http://docs.python-requests.org/en/latest/dev/contributing/) and our [development philosophy](http://docs.python-requests.org/en/latest/dev/philosophy/).
2.  Check for open issues or open a fresh issue to start a discussion
    around a feature idea or a bug. There is a [Contributor
    Friendly](https://github.com/requests/requests/issues?direction=desc&labels=Contributor+Friendly&page=1&sort=updated&state=open)
    tag for issues that should be ideal for people who are not very
    familiar with the codebase yet.
3.  Fork [the repository](https://github.com/requests/requests) on
    GitHub to start making your changes to the **master** branch (or
    branch off of it).
4.  Write a test which shows that the bug was fixed or that the feature
    works as expected.
5.  Send a pull request and bug the maintainer until it gets merged and
    published. :) Make sure to add yourself to
    [AUTHORS](https://github.com/requests/requests/blob/master/AUTHORS.rst).





%package -n python3-%{pkgname}
# Auto Python dependency
BuildRequires:  python3-devel
# Automatic runtime dependency generator
%?python_enable_dependency_generator

Summary: %{summary}
%description -n python3-%{pkgname}
Requests: HTTP for Humans™
==========================

[![image](https://img.shields.io/pypi/v/requests.svg)](https://pypi.org/project/requests/)
[![image](https://img.shields.io/pypi/l/requests.svg)](https://pypi.org/project/requests/)
[![image](https://img.shields.io/pypi/pyversions/requests.svg)](https://pypi.org/project/requests/)
[![codecov.io](https://codecov.io/github/requests/requests/coverage.svg?branch=master)](https://codecov.io/github/requests/requests)
[![image](https://img.shields.io/github/contributors/requests/requests.svg)](https://github.com/requests/requests/graphs/contributors)
[![image](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/kennethreitz)

Requests is the only *Non-GMO* HTTP library for Python, safe for human
consumption.

![image](https://farm5.staticflickr.com/4317/35198386374_1939af3de6_k_d.jpg)

Behold, the power of Requests:

``` {.sourceCode .python}
>>> import requests
>>> r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
>>> r.status_code
200
>>> r.headers['content-type']
'application/json; charset=utf8'
>>> r.encoding
'utf-8'
>>> r.text
u'{"type":"User"...'
>>> r.json()
{u'disk_usage': 368627, u'private_gists': 484, ...}
```

See [the similar code, sans Requests](https://gist.github.com/973705).

[![image](https://raw.githubusercontent.com/requests/requests/master/docs/_static/requests-logo-small.png)](http://docs.python-requests.org/)

Requests allows you to send *organic, grass-fed* HTTP/1.1 requests,
without the need for manual labor. There's no need to manually add query
strings to your URLs, or to form-encode your POST data. Keep-alive and
HTTP connection pooling are 100% automatic, thanks to
[urllib3](https://github.com/shazow/urllib3).

Besides, all the cool kids are doing it. Requests is one of the most
downloaded Python packages of all time, pulling in over 11,000,000
downloads every month. You don't want to be left out!

Feature Support
---------------

Requests is ready for today's web.

-   International Domains and URLs
-   Keep-Alive & Connection Pooling
-   Sessions with Cookie Persistence
-   Browser-style SSL Verification
-   Basic/Digest Authentication
-   Elegant Key/Value Cookies
-   Automatic Decompression
-   Automatic Content Decoding
-   Unicode Response Bodies
-   Multipart File Uploads
-   HTTP(S) Proxy Support
-   Connection Timeouts
-   Streaming Downloads
-   `.netrc` Support
-   Chunked Requests

Requests officially supports Python 2.7 & 3.4–3.7, and runs great on
PyPy.

Installation
------------

To install Requests, simply use [pipenv](http://pipenv.org/) (or pip, of
course):

``` {.sourceCode .bash}
$ pipenv install requests
✨🍰✨
```

Satisfaction guaranteed.

Documentation
-------------

Fantastic documentation is available at
<http://docs.python-requests.org/>, for a limited time only.

How to Contribute
-----------------

1.  Become more familiar with the project by reading our [Contributor's Guide](http://docs.python-requests.org/en/latest/dev/contributing/) and our [development philosophy](http://docs.python-requests.org/en/latest/dev/philosophy/).
2.  Check for open issues or open a fresh issue to start a discussion
    around a feature idea or a bug. There is a [Contributor
    Friendly](https://github.com/requests/requests/issues?direction=desc&labels=Contributor+Friendly&page=1&sort=updated&state=open)
    tag for issues that should be ideal for people who are not very
    familiar with the codebase yet.
3.  Fork [the repository](https://github.com/requests/requests) on
    GitHub to start making your changes to the **master** branch (or
    branch off of it).
4.  Write a test which shows that the bug was fixed or that the feature
    works as expected.
5.  Send a pull request and bug the maintainer until it gets merged and
    published. :) Make sure to add yourself to
    [AUTHORS](https://github.com/requests/requests/blob/master/AUTHORS.rst).





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
%{python3_sitelib}/requests-2.22.0.dist-info/
%{python3_sitelib}/requests/


# todo: missing %license (get from manifest.in maybe)
# todo: missing %doc (not that important)

%changelog
* Tue Feb 27 2018 Lumír Balhar <lbalhar@redhat.com> - 2.22.0-1
- Some changelog entry
~~~

### Build source and binary RPM
[rpm guide](https://fedoraproject.org/wiki/How_to_create_a_GNU_Hello_RPM_package)  
[simpler Fedora specific guide](https://docs.fedoraproject.org/en-US/quick-docs/creating-rpm-packages/)

### What do we do

For now we get information from pypi. Then install package to virtual environment to get list of files and we
merge them. The preparation of build dependencies is handled by [Fedora macros](https://src.fedoraproject.org/rpms/pyproject-rpm-macros).
