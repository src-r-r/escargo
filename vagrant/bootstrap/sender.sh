#!/bin/bash

# Prepare IRedMail Server

IREDMAIL_VERSION=0.9.8
IREDMAIL_INSTALL=iRedMail.sh


sudo apt update
sudo mkdir -p /opt/iredmail
cd /opt/iredmail
sudo wget https://bitbucket.org/zhb/iredmail/downloads/iRedMail-${IREDMAIL_VERSION}.tar.bz2
sudo tar -xvjf iRedMail-${IREDMAIL_VERSION}.tar.bz2
cd iRedMail-${IREDMAIL_VERSION}

# We should have the config in the vagrant subdirectory of this project.
cp /vagrant/vagrant/bootstrap/sender-config config

# Use escargo4testing for all passwords
# Use sender.escargo for the mail domainname.

echo "Setting hostname to `sender.escargo`"
sudo sh -c 'hostname mail-sender.escargo'
sudo sh -c 'echo "# Added as part of vagrant provisioning" >> /etc/hosts'
sudo sh -c 'echo "127.0.0.1   mail-sender.escargo mail-sender localhost" >> /etc/hosts'

export AUTO_USE_EXISTING_CONFIG_FILE=y \
    AUTO_INSTALL_WITHOUT_CONFIRM=y \
    AUTO_CLEANUP_REMOVE_SENDMAIL=y \
    AUTO_CLEANUP_REMOVE_MOD_PYTHON=y \
    AUTO_CLEANUP_REPLACE_FIREWALL_RULES=y \
    AUTO_CLEANUP_RESTART_IPTABLES=y \
    AUTO_CLEANUP_REPLACE_MYSQL_CONFIG=y \
    AUTO_CLEANUP_RESTART_POSTFIX=n

sudo sh -c "echo export status_check_new_iredmail='DONE' > .status"
sudo sh -c "echo export status_fetch_pkgs='DONE' >> .status"
sudo sh -c "echo export status_fetch_misc='DONE' >> .status"
sudo sh -c "echo export status_fetch_misc='DONE' >> .status"

sudo sh -c 'AUTO_USE_EXISTING_CONFIG_FILE=y \
    AUTO_INSTALL_WITHOUT_CONFIRM=y \
    AUTO_CLEANUP_REMOVE_SENDMAIL=y \
    AUTO_CLEANUP_REMOVE_MOD_PYTHON=y \
    AUTO_CLEANUP_REPLACE_FIREWALL_RULES=y \
    AUTO_CLEANUP_RESTART_IPTABLES=y \
    AUTO_CLEANUP_REPLACE_MYSQL_CONFIG=y \
    AUTO_CLEANUP_RESTART_POSTFIX=n \
    bash iRedMail.sh'

echo "Rebooting system."
echo "To open email, go to http://22.22.22.22/iredadmin/"
sudo reboot
