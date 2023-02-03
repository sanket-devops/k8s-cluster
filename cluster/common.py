import json
import time
import settings
from cluster.modules.ssh import ssh_conn


def Setup_All_Nodes(servers):
    print("Step 2:\n##################################################{ Common Setup Started On All Nodes }##################################################")
    for server in servers:
        id = server["id"]
        host = server["host"]
        username = server["username"]
        password = server["password"]
        hostname = server["hostname"]
        role = server["role"]
        master = server["master"]
        print("========================================>[ {} = {} ]<========================================".format(hostname, host))
        
        def Set_Hostname():
            print(">>>>>>>>>>>>>>>>>>>>( Set Hostname )=>( {} = {} )<<<<<<<<<<<<<<<<<<<<".format(hostname, host))
            commandsArr = ["hostnamectl set-hostname {}".format(hostname),"cat /etc/hostname"]
            res = ssh_conn(host, username, password, commandsArr)
            print("Hostname set...")
        # Set_Hostname()

        def Set_Hosts():
            print(">>>>>>>>>>>>>>>>>>>>>( Add Host Entry )=>( {} = {} )<<<<<<<<<<<<<<<<<<<<".format(hostname, host))
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
        # Set_Hosts()

        def Swap_Off():
            print(">>>>>>>>>>>>>>>>>>>>( Swap Off )=>( {} = {} )<<<<<<<<<<<<<<<<<<<<".format(hostname, host))
            commandsArr = ["sed -i '/swap/d' /etc/fstab", "swapoff -a"]
            res = ssh_conn(host, username, password, commandsArr)
            print("Disable and turn off SWAP")
        # Swap_Off()

        def Firewall_Disable():
            print(">>>>>>>>>>>>>>>>>>>>( Firewall Disable )=>( {} = {} )<<<<<<<<<<<<<<<<<<<<".format(hostname, host))
            commandsArr = ["systemctl disable --now ufw"]
            res = ssh_conn(host, username, password, commandsArr)
            print("Stop and Disable firewall")
        # Firewall_Disable()

        def Install_Packages():
            print(">>>>>>>>>>>>>>>>>>>>( Install Packages )=>( {} = {} )<<<<<<<<<<<<<<<<<<<<".format(hostname, host))
            commandsArr = ["apt update", "apt-get install -y net-tools htop curl git apt-transport-https ca-certificates wget"]
            res = ssh_conn(host, username, password, commandsArr)
            print("Require packages are installed...")
        # Install_Packages()

        def Kernal_Modules():
            print(">>>>>>>>>>>>>>>>>>>>( Load K8S Network Kernal Modules )=>( {} = {} )<<<<<<<<<<<<<<<<<<<<".format(hostname, host))
            commandsArr = [
                "cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf\noverlay\nbr_netfilter\nEOF",
                "modprobe overlay", "modprobe br_netfilter", 
                "cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf\nnet.bridge.bridge-nf-call-iptables  = 1\nnet.bridge.bridge-nf-call-ip6tables = 1\nnet.ipv4.ip_forward                 = 1\nEOF", 
                "sysctl --system"
                ]
            res = ssh_conn(host, username, password, commandsArr)
            print("Kernal modules Loaded...")
        # Kernal_Modules()

        def Install_Runtime():
            print(">>>>>>>>>>>>>>>>>>>>( Install Container Runtime )=>( {} = {} )<<<<<<<<<<<<<<<<<<<<".format(hostname, host))
            commandsArr = [
                "wget https://github.com/containerd/containerd/releases/download/v{}/containerd-{}-linux-amd64.tar.gz -O containerd-{}-linux-amd64.tar.gz".format(settings.containerd, settings.containerd, settings.containerd),
                "tar Cxzvf /usr/local containerd-{}-linux-amd64.tar.gz".format(settings.containerd),
                "wget -P /etc/systemd/system https://raw.githubusercontent.com/containerd/containerd/main/containerd.service",
                "mkdir /etc/containerd",
                "echo '{}' > /etc/containerd/config.toml".format(settings.Containerd_Config.replace("localhost", server["local-registry"])),
                "systemctl daemon-reload && systemctl enable --now containerd && systemctl restart containerd",
                "wget https://github.com/opencontainers/runc/releases/download/v{}/runc.amd64 -O runc.amd64".format(settings.runc),
                "install -m 755 runc.amd64 /usr/local/sbin/runc"
                ]
            res = ssh_conn(host, username, password, commandsArr)
            print("Container Runtime Installed...")
        # Install_Runtime()

        def Install_Kubernetes():
            print(">>>>>>>>>>>>>>>>>>>>( Install Kubernetes Components )=>( {} = {} )<<<<<<<<<<<<<<<<<<<<".format(hostname, host))
            commandsArr = [
                "curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg",
                "echo 'deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main' | tee /etc/apt/sources.list.d/kubernetes.list",
                "dpkg --configure -a",
                "apt-get update",
                "apt-get install -y kubeadm={}-00 kubelet={}-00 kubectl={}-00".format(settings.kubernetes, settings.kubernetes, settings.kubernetes)
                ]
            res = ssh_conn(host, username, password, commandsArr)
            print("Kubernetes Components Installed...")
        # Install_Kubernetes()

        def Reboot_Server():
            print(">>>>>>>>>>>>>>>>>>>>( Reboot Server )=>( {} = {} )<<<<<<<<<<<<<<<<<<<<".format(hostname, host))
            commandsArr = [
                "reboot"
                ]
            res = ssh_conn(host, username, password, commandsArr)
            time.sleep(5)
            print("Server Rebooting...")
        # Reboot_Server()

        def Check_Server_Back_Online():
            online  = False
            counter = 0
            while counter <= 4 :
                counter = counter + 1
                commandsArr = [
                    "hostnamectl hostname"
                    ]
                res = ssh_conn(host, username, password, commandsArr)
                for commands in res:
                    for output in commands:
                        if output == hostname:
                            print("{} = {} > Server Back Online Connected...".format(hostname, host))
                            online = True
                            break
                if online:
                    break
                else:
                    print(counter, ".: Connectiong...")
        Check_Server_Back_Online()
    print("##################################################{ Common Setup Finished On All Nodes }##################################################")