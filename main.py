import json
import settings
from cluster.common import setup_all_nodes

servers = json.load(settings.servers)


setup_all_nodes(servers)