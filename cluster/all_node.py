import json
from cluster.modules.ssh import ssh_conn


def setup_all_node(servers):
    for server in servers:
        id = server["id"]
        host = server["host"]
        username = server["username"]
        password = server["password"]
        hostname = server["hostname"]
        role = server["role"]
        master = server["master"]
        
        def set_hostname(server):
            print("====================>[Set Hostname]=>[ {} = {} ]<====================".format(hostname, host))
            commandsArr = ["hostnamectl set-hostname {}".format(hostname),"cat /etc/hostname"]
            res = ssh_conn(host, username, password, commandsArr)
            print(res)
        # set_hostname(server)

        def set_hosts(servers):
            print("====================>[Set Hosts]=>[ {} = {} ]<====================".format(hostname, host))
            for node in servers:
                def set_hostEntry():
                    commandsArr = ["cat >>/etc/hosts<<EOF\n{}    {}\nEOF".format(node["host"], node["hostname"]),"cat /etc/hosts"]
                    res = ssh_conn(host, username, password, commandsArr)
                    # print(res)
                    return res
                commands_check = ["cat /etc/hosts | grep '{}    {}'".format(node["host"], node["hostname"])]
                res = ssh_conn(host, username, password, commands_check)
                # print(len(res))
                for resData in res:
                    # print(len(data))
                    if len(resData) == 0:
                        set_hostEntry()
                        print("Host entery set...")
                    else:
                        print("Host entery already set...")
        # set_hosts(servers)

        def swap_off(server):
            print("====================>[Set Hostname]=>[ {} = {} ]<====================".format(hostname, host))
            commandsArr = ["sed -i '/swap/d' /etc/fstab", "swapoff -a"]
            res = ssh_conn(host, username, password, commandsArr)
            print(res)
        swap_off(server)


    