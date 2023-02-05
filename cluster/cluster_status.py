import json
import time
import settings
from cluster.modules.ssh import ssh_conn

def Cluster_Status(servers):
    print("Step 4:\n##################################################{ Cluster Status }##################################################\n")
    for server in servers:
        id = server["id"]
        host = server["host"]
        username = server["username"]
        password = server["password"]
        hostname = server["hostname"]
        role = server["role"]
        master = server["master"]
        if master :
            print("========================================>[ {} = {} ]<========================================".format(hostname, host))

            def K8S_Status():
                print("\n>>>>>>>>>>>>>>>>>>>>( Kubernetes Cluster Status )=>( {} = {} )<<<<<<<<<<<<<<<<<<<<\n".format(hostname, host))
                commandsArr = ["kubectl --kubeconfig /etc/kubernetes/admin.conf get nodes -o wide", "kubectl --kubeconfig /etc/kubernetes/admin.conf get all --all-namespaces -o wide"]
                res = ssh_conn(host, username, password, commandsArr)
                for commands in res:
                    for output in commands:
                        print(output)
                print("\n** To start using your cluster, you need to run the following as a regular user **")
                print("\nmkdir -p $HOME/.kube")
                print("\nsudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config")
                print("\nsudo chown $(id -u):$(id -g) $HOME/.kube/config")
                print("\n##################################################[ Cluster Setup Completed... ( ** Please Check Above Cluster Status ** )]##################################################\n")
            K8S_Status()