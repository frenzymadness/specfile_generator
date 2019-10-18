FROM fedora:rawhide
RUN dnf install -y rpm-build rpm-devel rpmlint rpmdevtools python3-requests python3-jinja2
RUN dnf install -y python3-pip --nogpgcheck
RUN rpmdev-setuptree
COPY ./ /app/
WORKDIR /app/
RUN python3 -m pip install .
CMD sh buildscript.sh requests