import json
from cluster.modules.ssh import ssh_conn


def setup_all_node(servers):
    for server in servers:
        id = server["id"]
        host = server["host"]
        username = server["username"]
        password = server["password"]
        hostname = server["hostname"]
        role = server["role"]
        master = server["master"]
        print("========================================>[ {} = {} ]<========================================".format(hostname, host))
        def set_hostname(server):
            print(">>>>>>>>>>>>>>>>>>>>[Set Hostname]=>[ {} = {} ]<<<<<<<<<<<<<<<<<<<<".format(hostname, host))
            commandsArr = ["hostnamectl set-hostname {}".format(hostname),"cat /etc/hostname"]
            res = ssh_conn(host, username, password, commandsArr)
            print("Hostname set...")
        # set_hostname(server)

        def set_hosts(servers):
            print(">>>>>>>>>>>>>>>>>>>>>[Add Host Entry]=>[ {} = {} ]<<<<<<<<<<<<<<<<<<<<".format(hostname, host))
            for node in servers:
                def set_hostEntry():
                    commandsArr = ["cat >>/etc/hosts<<EOF\n{}    {}\nEOF".format(node["host"], node["hostname"]),"cat /etc/hosts"]
                    res = ssh_conn(host, username, password, commandsArr)
                    return res
                commands_check = ["cat /etc/hosts | grep '{}    {}'".format(node["host"], node["hostname"])]
                res = ssh_conn(host, username, password, commands_check)
                for resData in res:
                    if len(resData) == 0:
                        set_hostEntry()
                        print("Host entery add...")
                    else:
                        print("Host entery already added...")
        # set_hosts(servers)

        def swap_off():
            print(">>>>>>>>>>>>>>>>>>>>[Swap Off]=>[ {} = {} ]<<<<<<<<<<<<<<<<<<<<".format(hostname, host))
            commandsArr = ["sed -i '/swap/d' /etc/fstab", "swapoff -a"]
            res = ssh_conn(host, username, password, commandsArr)
            print("Disable and turn off SWAP")
        # swap_off()

        def firewall_disable():
            print(">>>>>>>>>>>>>>>>>>>>[Firewall Disable]=>[ {} = {} ]<<<<<<<<<<<<<<<<<<<<".format(hostname, host))
            commandsArr = ["systemctl disable --now ufw"]
            res = ssh_conn(host, username, password, commandsArr)
            print("Stop and Disable firewall")
        # firewall_disable()

        def install_packages():
            print(">>>>>>>>>>>>>>>>>>>>[Install Packages]=>[ {} = {} ]<<<<<<<<<<<<<<<<<<<<".format(hostname, host))
            commandsArr = ["apt update", "apt-get install -y net-tools htop curl git apt-transport-https ca-certificates wget"]
            res = ssh_conn(host, username, password, commandsArr)
            print("Require packages are installed...")
        # install_packages()

        def kernal_modules():
            print(">>>>>>>>>>>>>>>>>>>>[Load Kernal Modules]=>[ {} = {} ]<<<<<<<<<<<<<<<<<<<<".format(hostname, host))
            commandsArr = ["cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf\noverlay\nbr_netfilter\nEOF", "modprobe overlay", "modprobe br_netfilter", "cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf\nnet.bridge.bridge-nf-call-iptables  = 1\nnet.bridge.bridge-nf-call-ip6tables = 1\nnet.ipv4.ip_forward                 = 1\nEOF", "sysctl --system"]
            res = ssh_conn(host, username, password, commandsArr)
            print("Load kernal modules...")
        # kernal_modules()
    