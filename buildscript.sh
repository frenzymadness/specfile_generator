#!/usr/bin/env bash
echo "Generating specfile"
python3 gen_spec.py --debug $1
cp $1.spec /root/rpmbuild/SPECS
cd /root/rpmbuild/

echo "Downloading source"
spectool -g -R /root/rpmbuild/SPECS/*
dnf install -y --nogpgcheck 'dnf-command(builddep)'

echo "Instaling dependencies for dependency generator"
dnf builddep -y SPECS/*.spec
echo "Checking if dependencies are on system"
rpmbuild -br SPECS/*.spec
file=$(compgen -G "SRPMS/*nosrc*")
# We need to loop through dependencies and their dependencies so on ... to install them
while [ -f "$file" ]
do
echo "Installing generated dependencies"
dnf builddep -y SRPMS/*
rm -f SRPMS/*
echo "Checking if dependencies are on system"
rpmbuild -br SPECS/*.spec
done

echo "Building rpm package"
rpmbuild -ba SPECS/*.spec || exit 1

echo "Trying to install rpm package/s of $1"
rpmfiles=$(find ./RPMS -name "*rpm")
dnf install -y --nogpgcheck $rpmfiles || exit 1