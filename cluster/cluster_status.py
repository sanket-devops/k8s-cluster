import json
import time
import settings
import os
os.system("")
from cluster.modules.ssh import ssh_conn

def Cluster_Status(servers):
    print(settings.COLOR["GREEN"], "Step 4:\n##################################################{ Cluster Status }##################################################\n", settings.COLOR["ENDC"])
    for server in servers:
        id = server["id"]
        host = server["host"]
        username = server["username"]
        password = server["password"]
        hostname = server["hostname"]
        role = server["role"]
        master = server["master"]
        if master :
            print(settings.COLOR["YELLOW"], "========================================>[ {} = {} ]<========================================".format(hostname, host), settings.COLOR["ENDC"])

            def K8S_Status():
                print(settings.COLOR["BLUE"], "\n>>>>>>>>>>>>>>>>>>>>( Kubernetes Cluster Status )=>( {} = {} )<<<<<<<<<<<<<<<<<<<<\n".format(hostname, host), settings.COLOR["ENDC"])
                commandsArr = ["kubectl --kubeconfig /etc/kubernetes/admin.conf get nodes -o wide", "kubectl --kubeconfig /etc/kubernetes/admin.conf get all --all-namespaces -o wide", "chmod 644 /etc/kubernetes/admin.conf"]
                res = ssh_conn(host, username, password, commandsArr)
                for commands in res:
                    for output in commands:
                        print(output)
                print("\n** To start using your cluster, you need to run the following as a regular user **")
                print("\nmkdir -p $HOME/.kube")
                print("\nsudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config")
                print("\nsudo chown $(id -u):$(id -g) $HOME/.kube/config")
                print("echo 'source <(kubectl completion bash)' >> ~/.bashrc && echo 'alias k=kubectl'>> ~/.bashrc && echo 'export KUBE_EDITOR=nano'>> ~/.bashrc && source ~/.bashrc")
                print(settings.COLOR["GREEN"], "\n##################################################[ Cluster Setup Completed... ( ** Please Check Above Cluster Status ** )]##################################################\n", settings.COLOR["ENDC"])
            K8S_Status()
