#!/usr/bin/env bash

PUBKEY=$(cat /home/kali/.ssh/id_rsa.pub)
PASSWORD="admin"

nodes=(
  "k8s-node1 00:16:3e:aa:bb:01 192.168.56.101"
  "k8s-node2 00:16:3e:aa:bb:02 192.168.56.102"
  "k8s-node3 00:16:3e:aa:bb:03 192.168.56.103"
)

for node in "${nodes[@]}"; do
  name=$(echo $node | awk '{print $1}')
  mac=$(echo $node | awk '{print $2}')
  ip=$(echo $node | awk '{print $3}')

  echo "Creating $name with MAC $mac and applying cloud-init"

  # use a variable to hold the cloud-init content
  cloudinit=$(cat <<EOF
#cloud-config
hostname: $name
ssh_pwauth: true
disable_root: false
users:
  - name: root
    shell: /bin/bash
    sudo: ALL=(ALL) NOPASSWD:ALL
    lock_passwd: false
    passwd: "\$6\$yTu5qDzI\$PEtNTOQzL0yOlfqbsJ50ZqVxbgD38Lx9hyWQwnQ48yptHLRrgINs0k/fNwD1BB6nM8U4JhCl15to6OdEIQENb/"
    ssh_authorized_keys:
      - "$PUBKEY"
package_update: true
package_upgrade: true
packages:
  - net-tools
  - iputils-ping
  - openssh-server
write_files:
  - path: /etc/ssh/sshd_config
    content: |
      Port 22
      Protocol 2
      PermitRootLogin yes
      PasswordAuthentication yes
      PubkeyAuthentication yes
      UsePAM yes
      ChallengeResponseAuthentication no
      PrintMotd no
      AcceptEnv LANG LC_*
      Subsystem sftp /usr/lib/openssh/sftp-server
  - path: /etc/netplan/50-cloud-init.yaml
    permissions: '0644'
    content: |
      network:
        version: 2
        ethernets:
          eth0:
            dhcp4: no
            addresses:
              - $ip/24
            gateway4: 192.168.56.1
            nameservers:
              addresses: [8.8.8.8,8.8.4.4]
runcmd:
  - netplan apply
  - systemctl restart ssh
  - echo "root:$PASSWORD" | chpasswd
EOF
)

  lxc launch ubuntu:22.04 $name --profile default --profile k8s \
    -c user.user-data="$cloudinit"

  echo "$name launched with static IP $ip"
done

echo "Waiting for containers to settle..."
sleep 120

for node in "${nodes[@]}"; do
  name=$(echo $node | awk '{print $1}')
  echo "Restarting $name..."
  lxc restart "$name"
  sleep 10
  echo "Checking internet on $name..."
  lxc exec "$name" -- ping -c 3 google.com
done

echo "All containers launched successfully."
lxc list
