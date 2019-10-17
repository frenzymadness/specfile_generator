#!/usr/bin/env bash
python3 gen_spec.py $1
cp $1.spec /root/rpmbuild/SPECS
cd /root/rpmbuild/SOURCES
spectool -g /root/rpmbuild/SPECS/*
cd /root/rpmbuild/
rpmbuild -br SPECS/*.spec
dnf install -y --nogpgcheck 'dnf-command(builddep)'
dnf builddep -y SPECS/*
rpmbuild -br --nodeps SPECS/*.spec
file=$(compgen -G "SRPMS/*nosrc*")
while [ -f "$file" ]
do
dnf builddep -y SRPMS/*
rm -f SRPMS/*
rpmbuild -br SPECS/*.spec
done
rpmbuild -ba SPECS/*.spec

rpmfile=$(find ./RPMS -name "*rpm")
if [ -n "$rpmfile" ]
then
    exit 0
else
    echo "unsuccessfull build of $1"
    exit 1
fi