global servers
servers = [
    {
        "id": 1,
        "host": "10.0.2.101",
        "username": "root",
        "password": "admin",
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
        "hostname": "node2",
        "local-registry": "10.0.2.101",
        "role": "worker",
        "master": False
    }
]
global containerd
containerd = "1.7.8"
global runc
runc = "1.1.10"
global kubernetes_minor
kubernetes_minor = "1.28"
global kubernetes
kubernetes = "1.28.4"
global kubernetes_semantic
kubernetes_semantic = "1.1"
global Containerd_Config
Containerd_Config = open("./Container-Runtimes/containerd/containerd_1.7.8.toml").read()
global Node_Join

# K8S Network Configuration
global network_cidr
network_cidr = "10.244.0.0/16"

# https://docs.tigera.io/calico/latest/getting-started/kubernetes/self-managed-onprem/onpremises#install-calico
global tigera_operator_local_path
tigera_operator_local_path = "./network/calico_v3.26.4/tigera-operator.yaml"
global tigera_operator_remote_path
tigera_operator_remote_path = "/etc/kubernetes/network/calico/tigera-operator.yaml"
global custom_resources
custom_resources = open("./network/calico_v3.26.4/custom-resources.yaml").read()

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
