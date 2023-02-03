global containerd
containerd = "1.6.16"
global runc
runc = "1.1.4"
global kubernetes
kubernetes = "1.26.1"
global servers
servers = open("servers.json")
global Containerd_Config
Containerd_Config = open("containerd_1.6.16.toml").read()