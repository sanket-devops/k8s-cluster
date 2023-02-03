import json
import settings
from cluster.common import Setup_All_Nodes
from cluster.master import Setup_Cluster

servers = json.load(settings.servers)


Setup_All_Nodes(servers)
Setup_Cluster(servers)
# Join_Nodes(servers)