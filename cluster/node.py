import json
import time
import settings
import os
os.system("")
from cluster.modules.ssh import ssh_conn

def Join_Nodes(servers):
    print(settings.COLOR["GREEN"], "Step 3:\n##################################################{ Join Worker Nodes With The Cluster }##################################################\n", settings.COLOR["ENDC"])
    for server in servers:
        id = server["id"]
        host = server["host"]
        username = server["username"]
        password = server["password"]
        hostname = server["hostname"]
        role = server["role"]
        master = server["master"]
        if not master :
            print(settings.COLOR["YELLOW"], "========================================>[ {} = {} ]<========================================".format(hostname, host), settings.COLOR["ENDC"])

            def Join_Node():
                print(settings.COLOR["BLUE"], "\n>>>>>>>>>>>>>>>>>>>>( Join This Node To The Cluster )=>( {} = {} )<<<<<<<<<<<<<<<<<<<<\n".format(hostname, host), settings.COLOR["ENDC"])
                commandsArr = ["{}".format(settings.Node_Join)]
                res = ssh_conn(host, username, password, commandsArr)
                for commands in res:
                    for output in commands:
                        print(output)
                time.sleep(30)
                print("\nNode Join Proccess Completed...\n")
            Join_Node()