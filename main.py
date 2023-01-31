import json
from cluster.all_node import setup_all_node

remote_servers = open("servers.json")
servers = json.load(remote_servers)


setup_all_node(servers)