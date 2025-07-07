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
        sshKey = None
        for path in server["keyFilePaths"]:
            expanded = os.path.expanduser(path)
            if os.path.exists(expanded):
                sshKey = expanded
                break  # found the first usable key
        if not sshKey:
            raise FileNotFoundError(
                f"No valid SSH key found in {server['keyFilePaths']}"
            )
        hostname = server["hostname"]
        role = server["role"]
        master = server["master"]
        if master:
            print(settings.COLOR["YELLOW"], "========================================>[ {} = {} ]<========================================".format(hostname, host), settings.COLOR["ENDC"])

            def Image_Pull():
                print(settings.COLOR["BLUE"], "\n>>>>>>>>>>>>>>>>>>>>( Preflight Check And Downloaded All Required Images )=>( {} = {} )<<<<<<<<<<<<<<<<<<<<\n".format(hostname, host), settings.COLOR["ENDC"])
                commandsArr = ["kubeadm config images pull"]
                res = ssh_conn(host, username, password, sshKey, commandsArr)
                # for commands in res:
                #     for output in commands:
                #         print(output)
                print("\nPreflight Check Passed: Downloaded All Required Images")
            Image_Pull()


            def Kubeadm_Cluster():
                print(settings.COLOR["BLUE"], "\n++++++++++++++++++++( Initialize Kubeadm Cluster )++++++++++++++++++++\n", settings.COLOR["ENDC"])
                commandsArr = ["kubeadm init --cri-socket=unix:///var/run/containerd/containerd.sock --pod-network-cidr={} --apiserver-advertise-address={} --apiserver-cert-extra-sans={} --node-name={} --kubernetes-version={} --ignore-preflight-errors=SystemVerification".format(settings.network_cidr, host, host, hostname, settings.kubernetes), "echo 'KUBECONFIG=/etc/kubernetes/admin.conf' >> /etc/environment"]
                res = ssh_conn(host, username, password, sshKey, commandsArr)
                # for commands in res:
                #     for output in commands:
                #         print(output)
                time.sleep(30)
                print("\nKubeadm Cluster Initialization Completed...")
            Kubeadm_Cluster()

            def Node_Join_Command():
                print(settings.COLOR["BLUE"], "\n++++++++++++++++++++( Generate Node Join Command )++++++++++++++++++++\n", settings.COLOR["ENDC"])
                commandsArr = ["kubeadm token create --print-join-command"]
                res = ssh_conn(host, username, password, sshKey, commandsArr)
                for commands in res:
                    for output in commands:
                        settings.Node_Join = output
                        # print(output)
                print("\nNode Join Command Generated...")
            Node_Join_Command()

            def Install_CNI():
                print(settings.COLOR["BLUE"], "\n++++++++++++++++++++( Initialize CNI )++++++++++++++++++++\n", settings.COLOR["ENDC"])

                cilium_script = f"""
CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/main/stable.txt)
CLI_ARCH=amd64
if [ "$(uname -m)" = "aarch64" ]; then CLI_ARCH=arm64; fi

curl -L --fail --remote-name-all https://github.com/cilium/cilium-cli/releases/download/${{CILIUM_CLI_VERSION}}/cilium-linux-${{CLI_ARCH}}.tar.gz{{,.sha256sum}}

sha256sum --check cilium-linux-${{CLI_ARCH}}.tar.gz.sha256sum

sudo tar xzvfC cilium-linux-${{CLI_ARCH}}.tar.gz /usr/local/bin

rm cilium-linux-${{CLI_ARCH}}.tar.gz{{,.sha256sum}}

cilium install --version {settings.cilium_version} --set ipam.operator.clusterPoolIPv4PodCIDRList="{{{settings.network_cidr}}}"
"""
                res = ssh_conn(host, username, password, sshKey, [cilium_script])

                # for commands in res:
                #     for output in commands:
                #         print(output)
                # time.sleep(60)
                print("\nCNI Installed...")
            Install_CNI()

            def Install_metrics_server():
                print(settings.COLOR["BLUE"], "\n++++++++++++++++++++( Install Metrics Server )++++++++++++++++++++\n", settings.COLOR["ENDC"])
                commandsArr = [
                    "mkdir -p /etc/kubernetes/metrics-server",
                    "echo '{}' > /etc/kubernetes/metrics-server/components.yaml".format(settings.metrics_server_components.replace("        - --metric-resolution=15s", "        - --metric-resolution=15s\n        - --kubelet-insecure-tls")),
                    "kubectl --kubeconfig /etc/kubernetes/admin.conf apply -f /etc/kubernetes/metrics-server/components.yaml"
                    ]
                res = ssh_conn(host, username, password, sshKey, commandsArr)

                # for commands in res:
                #     for output in commands:
                #         print(output)
                # time.sleep(50)
                print("\nMetrics Server Installed...")
            Install_metrics_server()

            def Taint_Node():
                commandsArr = ["kubectl --kubeconfig /etc/kubernetes/admin.conf taint nodes --all node-role.kubernetes.io/control-plane:NoSchedule-"]
                res = ssh_conn(host, username, password, sshKey, commandsArr)
                # for commands in res:
                #     for output in commands:
                #         print(output)
                print("\nControl-Plane Work Load Schedule On...")
            Taint_Node()
    print(settings.COLOR["GREEN"], "\n##################################################{ Cluster Setup Finished On Master Node }##################################################\n", settings.COLOR["ENDC"])