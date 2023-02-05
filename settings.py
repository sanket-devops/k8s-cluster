global containerd
containerd = "1.6.16"
global runc
runc = "1.1.4"
global kubernetes
kubernetes = "1.26.1"
global Containerd_Config
Containerd_Config = open("containerd_1.6.16.toml").read()
global Node_Join
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