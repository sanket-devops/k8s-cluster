# 1. Installing LXD from packages
| OS | Format | Command |
| -- | ------ | ------- |
| Linux | Snap | snap install lxd |
| Windows | Chocolatey | choco install lxc |
| macOS | Homebrew | brew install lxc |

## Add your user to the lxd group so you don’t need sudo:
```shell
echo $SHELL && ps -p $$
echo 'export PATH=$PATH:/snap/bin' >> /root/.zshrc
# echo 'export PATH=$PATH:/snap/bin' >> ~/.bashrc && source ~/.bashrc
source /root/.zshrc
sudo usermod -aG lxd $USER
newgrp lxd
```

**IMPORTANT! Sysctl setting on host linux machine**
Run the below command on the Linux host where you are running lxd containers. Otherwise kube-proxy pods will fail.
```shell
# sudo sysctl -w net.netfilter.nf_conntrack_max=262144

# Or make it persistent:
echo "net.netfilter.nf_conntrack_max=262144" >> /etc/sysctl.conf
sudo sysctl -p


# cat /proc/sys/net/netfilter/nf_conntrack_max
```

# 2. Configure LXD
```shell
lxd init


Would you like to use LXD clustering? (yes/no) [default=no]: 
Do you want to configure a new storage pool? (yes/no) [default=yes]: 
Name of the new storage pool [default=default]: 
Name of the storage backend to use (powerflex, btrfs, ceph, dir, lvm) [default=btrfs]: 
Create a new BTRFS pool? (yes/no) [default=yes]: 
Would you like to use an existing empty block device (e.g. a disk or partition)? (yes/no) [default=no]: 
Size in GiB of the new loop device (1GiB minimum) [default=22GiB]: 
Would you like to connect to a MAAS server? (yes/no) [default=no]: 
Would you like to create a new local network bridge? (yes/no) [default=yes]: 
What should the new bridge be called? [default=lxdbr0]: 
What IPv4 address should be used? (CIDR subnet notation, “auto” or “none”) [default=auto]: 
What IPv6 address should be used? (CIDR subnet notation, “auto” or “none”) [default=auto]: 
Would you like the LXD server to be available over the network? (yes/no) [default=no]: 
Would you like stale cached images to be updated automatically? (yes/no) [default=yes]: 
Would you like a YAML "lxd init" preseed to be printed? (yes/no) [default=no]:

```

# 3. Install the OS you'd like to use in your container
Command:
```shell
lxc launch <image_server>:<image_name> <instance_name>
```
Example:
```shell
lxc launch ubuntu:22.04 ubuntu1
```

# 4. Run commands
Command:
```shell
lxc exec <instance_name> -- <command />
```
Example:
```shell
lxc exec ubuntu1 -- bash
lxc exec ubuntu1 -- ping -c 3 8.8.8.8
```

**Containers do not have outgoing internet access&&
I applied the solution of this other thread Lxd uses iptables-legacy even if iptables-nft is default and that solved my problem :slight_smile:

which is basically to flush all the iptable rules. This is all I did -
```shell
for ipt in iptables iptables-legacy ip6tables ip6tables-legacy; do $ipt --flush; $ipt --flush -t nat; $ipt --delete-chain; $ipt --delete-chain -t nat; $ipt -P FORWARD ACCEPT; $ipt -P INPUT ACCEPT; $ipt -P OUTPUT ACCEPT; done

systemctl reload snap.lxd.daemon
```

# 5. lxc commands
```shell
lxc list
lxc stop ubuntu1 && lxc delete ubuntu1
```

# Start lxd containers
```shell
lxc launch ubuntu:22.04 k8s-node1 --profile k8s
```

## Convert the Script to Unix Line Endings (LF)
```shell
sudo apt install dos2unix
dos2unix up-lxd.sh
dos2unix launch_k8s_nodes.sh
dos2unix down-lxd.sh


# Then retry:
./up-lxd.sh
```


# Use proxy LXD device to expose ports lxd port to wsl 
```shell
lxc config device add my-cont http7070 proxy listen=tcp:0.0.0.0:7070 connect=tcp:127.0.0.1:7070
lxc config device add my-cont http8443 proxy listen=tcp:0.0.0.0:8443 connect=tcp:127.0.0.1:8444
```

# Cleanup added network
```shell
lxc config device remove my-cont http7070
```
