import time
import settings
import os
os.system("")
from cluster.modules.ssh import ssh_conn
from cluster.modules.sftp import sftp_conn

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
                # for commands in res:
                #     for output in commands:
                #         print(output)
                print("\nPreflight Check Passed: Downloaded All Required Images")
            Image_Pull()


            def Kubeadm_Cluster():
                print(settings.COLOR["BLUE"], "\n++++++++++++++++++++( Initialize Kubeadm Cluster )++++++++++++++++++++\n", settings.COLOR["ENDC"])
                commandsArr = ["kubeadm init --cri-socket=unix:///var/run/containerd/containerd.sock --pod-network-cidr={} --apiserver-advertise-address={} --apiserver-cert-extra-sans={} --node-name={} --kubernetes-version={}".format(settings.network_cidr, host, host, hostname, settings.kubernetes), "echo 'KUBECONFIG=/etc/kubernetes/admin.conf' >> /etc/environment"]
                res = ssh_conn(host, username, password, commandsArr)
                # for commands in res:
                #     for output in commands:
                #         print(output)
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
                        # print(output)
                print("\nNode Join Command Generated...")
            Node_Join_Command()

            def Install_CNI():
                print(settings.COLOR["BLUE"], "\n++++++++++++++++++++( Initialize CNI )++++++++++++++++++++\n", settings.COLOR["ENDC"])
                # Flannel network plugin
                # commandsArr = ["kubectl --kubeconfig /etc/kubernetes/admin.conf apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml"]
                # res = ssh_conn(host, username, password, commandsArr)
                
                # Calico as a network plugin
                commandsArr1 = ["mkdir -p /etc/kubernetes/network/calico"]
                res = ssh_conn(host, username, password, commandsArr1)

                # Upload tigera-operator.yaml file to remote server
                sftp_conn(host, username, password, settings.tigera_operator_local_path, settings.tigera_operator_remote_path, "upload")

                commandsArr2 = [
                    "echo '{}' > /etc/kubernetes/network/calico/custom-resources.yaml".format(settings.custom_resources.replace("192.168.0.0/16", settings.network_cidr)),
                    "kubectl --kubeconfig /etc/kubernetes/admin.conf create -f /etc/kubernetes/network/calico/tigera-operator.yaml",
                    "kubectl --kubeconfig /etc/kubernetes/admin.conf create -f /etc/kubernetes/network/calico/custom-resources.yaml"
                    ]
                res = ssh_conn(host, username, password, commandsArr2)

                # for commands in res:
                #     for output in commands:
                #         print(output)
                time.sleep(60)
                print("\nCNI Installed...")
            Install_CNI()

            def Install_metrics_server():
                print(settings.COLOR["BLUE"], "\n++++++++++++++++++++( Install Metrics Server )++++++++++++++++++++\n", settings.COLOR["ENDC"])
                commandsArr = [
                    "mkdir -p /etc/kubernetes/metrics-server",
                    "echo '{}' > /etc/kubernetes/metrics-server/components.yaml".format(settings.metrics_server_components.replace("        - --metric-resolution=15s", "        - --metric-resolution=15s\n        - --kubelet-insecure-tls")),
                    "kubectl --kubeconfig /etc/kubernetes/admin.conf apply -f /etc/kubernetes/metrics-server/components.yaml"
                    ]
                res = ssh_conn(host, username, password, commandsArr)

                # for commands in res:
                #     for output in commands:
                #         print(output)
                time.sleep(30)
                print("\nMetrics Server Installed...")
            Install_metrics_server()

            def Taint_Node():
                commandsArr = ["kubectl --kubeconfig /etc/kubernetes/admin.conf taint nodes --all node-role.kubernetes.io/control-plane:NoSchedule-"]
                res = ssh_conn(host, username, password, commandsArr)
                # for commands in res:
                #     for output in commands:
                #         print(output)
                print("\nControl-Plane Work Load Schedule On...")
            Taint_Node()
    print(settings.COLOR["GREEN"], "\n##################################################{ Cluster Setup Finished On Master Node }##################################################\n", settings.COLOR["ENDC"])