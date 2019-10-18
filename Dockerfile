FROM fedora:rawhide
RUN dnf install -y rpm-build rpm-devel rpmlint rpmdevtools python3-requests python3-jinja2 python3-pip --nogpgcheck
RUN rpmdev-setuptree
COPY ./ /app/
WORKDIR /app/
CMD sh buildscript.sh requests