import time
import settings
import os
os.system("")
from cluster.modules.ssh import ssh_conn

def Setup_Cluster(servers):
    print(settings.COLOR["GREEN"], "Step 2:\n##################################################{ Cluster Setup Started On Master Node }##################################################\n", settings.COLOR["ENDC"])
    for server in servers:
        id = server["id"]
        host = server["host"]
        username = server["username"]
        password = server["password"]
        hostname = server["hostname"]
        role = server["role"]
        master = server["master"]
        if master:
            print(settings.COLOR["YELLOW"], "========================================>[ {} = {} ]<========================================".format(hostname, host), settings.COLOR["ENDC"])

            def Image_Pull():
                print(settings.COLOR["BLUE"], "\n>>>>>>>>>>>>>>>>>>>>( Preflight Check And Downloaded All Required Images )=>( {} = {} )<<<<<<<<<<<<<<<<<<<<\n".format(hostname, host), settings.COLOR["ENDC"])
                commandsArr = ["kubeadm config images pull"]
                res = ssh_conn(host, username, password, commandsArr)
                for commands in res:
                    for output in commands:
                        print(output)
                print("\nPreflight Check Passed: Downloaded All Required Images")
            Image_Pull()


            def Kubeadm_Cluster():
                print(settings.COLOR["BLUE"], "\n++++++++++++++++++++( Initialize Kubeadm Cluster )++++++++++++++++++++\n", settings.COLOR["ENDC"])
                commandsArr = ["kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address={} --apiserver-cert-extra-sans={} --node-name={} --kubernetes-version={}".format(host, host, hostname, settings.kubernetes), "echo 'KUBECONFIG=/etc/kubernetes/admin.conf' >> /etc/environment"]
                res = ssh_conn(host, username, password, commandsArr)
                for commands in res:
                    for output in commands:
                        print(output)
                time.sleep(30)
                print("\nKubeadm Cluster Initialization Completed...")
            Kubeadm_Cluster()

            def Node_Join_Command():
                print(settings.COLOR["BLUE"], "\n++++++++++++++++++++( Generate Node Join Command )++++++++++++++++++++\n", settings.COLOR["ENDC"])
                commandsArr = ["kubeadm token create --print-join-command"]
                res = ssh_conn(host, username, password, commandsArr)
                for commands in res:
                    for output in commands:
                        settings.Node_Join = output
                        print(output)
                print("\nNode Join Command Generated...")
            Node_Join_Command()

            def Install_CNI():
                print(settings.COLOR["BLUE"], "\n++++++++++++++++++++( Initialize CNI )++++++++++++++++++++\n", settings.COLOR["ENDC"])
                commandsArr = ["kubectl --kubeconfig /etc/kubernetes/admin.conf apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml"]
                res = ssh_conn(host, username, password, commandsArr)
                for commands in res:
                    for output in commands:
                        print(output)
                time.sleep(30)
                print("\nCNI Installed...")
            Install_CNI()

            def Taint_Node():
                commandsArr = ["kubectl --kubeconfig /etc/kubernetes/admin.conf taint nodes --all node-role.kubernetes.io/control-plane:NoSchedule-"]
                res = ssh_conn(host, username, password, commandsArr)
                for commands in res:
                    for output in commands:
                        print(output)
                print("\nControl-Plane Work Load Schedule On...")
            Taint_Node()
    print(settings.COLOR["GREEN"], "\n##################################################{ Cluster Setup Finished On Master Node }##################################################\n", settings.COLOR["ENDC"])