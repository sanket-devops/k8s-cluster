#!/bin/bash

# Enable ssh password authentication
echo "Enable ssh password authentication"
sed -i 's/^PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
sed -i 's/.*PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config
sed -i 's/.*PubkeyAuthentication.*/PubkeyAuthentication yes/' /etc/ssh/sshd_config
# Enable powershell remote session
sed -i '$ a Subsystem powershell /usr/bin/pwsh -sshs -NoLogo' /etc/ssh/sshd_config

# Restart sshd
systemctl reload sshd
# systemctl restart sshd

# Set Root password
echo "Set root password"
echo -e "admin\nadmin" | passwd root >/dev/null 2>&1



# Install PowerShell

# Update the list of packages
apt-get update

# Install pre-requisite packages.
apt-get install -y wget apt-transport-https software-properties-common

# Download the Microsoft repository GPG keys
wget -q "https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb"

# Register the Microsoft repository GPG keys
dpkg -i packages-microsoft-prod.deb

# Update the list of packages after we added packages.microsoft.com
apt-get update

# Install PowerShell
apt-get install -y powershell