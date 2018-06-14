#!/bin/bash

###
# Provisioning BASH file for an Escargo microservice
###

PYTHON_VERSION=3

apt update
apt dist-upgrade -y

apt install -y python${PYTHON_VERSION} python3-pip

ESCARGO_PID=$(ps axf | grep flask | grep -v grep | awk '{print $1 }')

if [ -z ${ESCARGO_PID} ]; then
    echo "Escargo is not running, whew!"
else
    echo "Escargo is running, killing ${ESCARGO_PID}"
    kill -9 ${ESCARGO_PID}
fi;

echo [*] Copying project from host -> guest
rm -fr /opt/escargo
mkdir -p /opt/escargo

mkdir -p /var/log/escargo
chown -R vagrant:vagrant /var/log/escargo

PYTHON=$(which python3)
PIP=$(which pip3)

echo [*] python=${PYTHON}, pip=${PIP}

cp -vR /vagrant/src /opt/escargo
cp /vagrant/README.md /opt/escargo/
# Clean up any residual python files from the host
find -iname '*.pyc' -exec rm -fr {} \;
find -iname 'escargo.egg-info' -exec rm -fr {} \;
chown -R vagrant:vagrant /opt/escargo

cd /opt/escargo
echo [*] Installing Python requirements
${PIP} install -r /opt/escargo/src/requirements.txt

cd /opt/escargo/src
${PYTHON} setup.py develop

echo [*] Starting flask application

FLASK_APP=escargo.main ${PYTHON} -m flask run
