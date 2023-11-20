import paramiko
import sys
import settings
import os
os.system("")

def ssh_conn(host, username, password, commandsArr):
    try:
        hostName = host
        hostUser = username
        hostPass = password
        commands = commandsArr
        results = []
        os.system("ssh-keygen -R {} > /dev/null 2>&1".format(hostName))
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostName, username=hostUser, password=hostPass)
        for command in commands:
            print(settings.COLOR["CYAN"], "🚀 " + command, settings.COLOR["ENDC"], "\n")
            temp = []
            ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(command)
            for line in ssh_stdout:
                print(line)
                nRemove = line.strip('\n')
                temp.append(nRemove)
            results.append(temp)
    except:
        print("SSH Connection Timeout...")
    # print("Host: ", hostName,"\nData: ", results)
    return results