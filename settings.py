global servers
servers = [
    {
        "id": 1,
        "host": "10.0.2.101",
        "username": "root",
        "password": "admin",
        "keyFilePath": "C:/Users/sanket/.ssh/id_rsa",
        "hostname": "master",
        "local-registry": "10.0.2.101",
        "role": "master",
        "master": True
    },
    {
        "id": 2,
        "host": "10.0.2.102",
        "username": "root",
        "password": "admin",
        "keyFilePath": "C:/Users/sanket/.ssh/id_rsa",
        "hostname": "node1",
        "local-registry": "10.0.2.101",
        "role": "worker",
        "master": False
    },
    {
        "id": 3,
        "host": "10.0.2.103",
        "username": "root",
        "password": "admin",
        "keyFilePath": "C:/Users/sanket/.ssh/id_rsa",
        "hostname": "node2",
        "local-registry": "10.0.2.101",
        "role": "worker",
        "master": False
    }
]
global containerd
containerd = "2.1.3"
global runc
runc = "1.3.0"
global kubernetes_minor
kubernetes_minor = "1.32"
global kubernetes
kubernetes = "1.32.5"
global kubernetes_semantic
kubernetes_semantic = "1.1"
global Containerd_Config
Containerd_Config = open("./Container-Runtimes/containerd/containerd_{}.toml".format(containerd)).read()
global Node_Join

# K8S Network Configuration
global network_cidr
network_cidr = "192.168.0.0/16"
# network_cidr = "10.244.0.0/16"

# https://docs.tigera.io/calico/latest/getting-started/kubernetes/self-managed-onprem/onpremises#install-calico
global calico_version
calico_version = "v3.30.1"
global custom_resources
custom_resources = open("./network/calico_{}/custom-resources.yaml".format(calico_version)).read()

# K8S Metrics
# https://github.com/kubernetes-sigs/metrics-server
# kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
# kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.7.2/components.yaml
global metrics_server_version
metrics_server_version = "v0.7.2"
global metrics_server_components
metrics_server_components = open("./Metrics-Server/{}/components.yaml".format(metrics_server_version)).read()


global COLOR
COLOR = {
    "HEADER": "\033[95m",
    "BLUE": "\033[1;34m",
    "GREEN": "\033[1;32m",
    "RED": "\033[1;31m",
    "YELLOW": "\033[1;33m",
    "CYAN": "\033[1;36m",
    "ENDC": "\033[0m",
}
