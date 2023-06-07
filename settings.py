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
        "host": "192.168.120.121",
        "username": "root",
        "password": "Yxorp$07-Jun-2023%dorP",
        "hostname": "proxy-prod-master",
        "local-registry": "192.168.120.121",
        "role": "master",
        "master": True
    },
    {
        "id": 2,
        "host": "192.168.120.122",
        "username": "root",
        "password": "Yxorp$07-Jun-2023%dorP",
        "hostname": "proxy-prod-node1",
        "local-registry": "192.168.120.121",
        "role": "worker",
        "master": False
    },
    {
        "id": 3,
        "host": "192.168.120.129",
        "username": "root",
        "password": "Yxorp$07-Jun-2023%dorP",
        "hostname": "proxy-prod-node2",
        "local-registry": "192.168.120.121",
        "role": "worker",
        "master": False
    },
    {
        "id": 4,
        "host": "192.168.120.147",
        "username": "root",
        "password": "Yxorp$07-Jun-2023%dorP",
        "hostname": "proxy-prod-node3",
        "local-registry": "192.168.120.121",
        "role": "worker",
        "master": False
    }
]
