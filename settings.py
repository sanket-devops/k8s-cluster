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
        "host": "192.168.120.33",
        "username": "root",
        "password": "Dorp$3202%rrepo",
        "hostname": "operr-v3-prod2-master",
        "local-registry": "192.168.120.33",
        "role": "master",
        "master": True
    },
    {
        "id": 2,
        "host": "192.168.120.34",
        "username": "root",
        "password": "Dorp$3202%rrepo",
        "hostname": "operr-v3-prod2-node1",
        "local-registry": "192.168.120.33",
        "role": "worker",
        "master": False
    },
    {
        "id": 3,
        "host": "192.168.120.35",
        "username": "root",
        "password": "Dorp$3202%rrepo",
        "hostname": "operr-v3-prod2-node2",
        "local-registry": "192.168.120.33",
        "role": "worker",
        "master": False
    }
]
