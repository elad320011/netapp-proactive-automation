import paramiko
import re

def proactive(hostname_netapp,address):
    print("")
    print(f"{hostname_netapp}-{address}-")
    print("\n")
    errors = ["offline", "degraded", "speamonffline", "nodeffline",
    "rebooting", "unknown", "updating", "unreachable", "okithuppressed", "false",
    "down","partial", "none","warning","error","critical","standbyower"]
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=address, username='Readrix', password='txyrydh440!')
    except:
        print(f"Unable to connect to {hostname_netapp} - {address}. Please check!\n")
        return
    #system health alert show
    stdin, stdout, stderr = ssh_client.exec_command("system health alert show")
    output = stdout.readlines()
    if "This table is currently empty." not in output[2].split("\r"):
        print("health error. please check:\n")
        for t in output:
            print(t)
    else:
        print("No Health Errors.\n")

    #system health subsystem show
    stdin, stdout, stderr = ssh_client.exec_command("system health subsystem show")
    output = stdout.readlines()

    for g in output:
        for t in errors:
            if t in g.split("\r")[0].split(" "):
                print("subsystem error. please check:\n")
                print(g)


    #net int show
    stdin, stdout, stderr = ssh_client.exec_command("net int show")
    output = stdout.readlines()
    lif_status=True
    statusadmin = ""
    for g in output:
        try:
            statusadmin = (g.split(" "))[].split("/")
        except:
            None
        for t in errors:
            if t in (g.split(" ")[]) or t in statusadmin:
                print("lif health is not ok:\n")
                print(g)
                lif_status=False
    if lif_status==True:
        print("All lifs are healthy.\n")


    #net port show
    stdin, stdout, stderr = ssh_client.exec_command("net port show")
    output = stdout.readlines()
    statusadmin = ""
    print("Checking ports...\n")
    port_status=True
    for g in output:
        try:
            statusadmin = (g.split(" ")[])
            if statusadmin!="up":
                try:
                    statusadmin = (g.split(" ")[])
                    
                except:
                    None
        except:
            None

        
        for t in errors:
            if (t in (g.split(" ")[])) or (t in statusadmin):
                print(g)
                port_status=False
    if port_status==True:
        print("All ports are OK.\n")

    #event log show everity emergency
    stdin, stdout, stderr = ssh_client.exec_command("event log show everity emergency")
    output = stdout.readlines()
    if "There are no entries matching your query." not in output[2].split("\r"):
        print("Emergency errors. please check:\n")
        for t in output:
            print(t)
    else:
        print("No emergency errors.\n")

    #broken disks
    stdin, stdout, stderr = ssh_client.exec_command("disk show roken")
    output = stdout.readlines()

    if "There are no entries matching your query." not in output[2].split("\r"):
        print("Broken disks. please check:\n")
        for t in output:
            print(t)
    else:
        print("No broken disks.\n")

    #aggregates with high usage
    stdin, stdout, stderr = ssh_client.exec_command("aggr show")
    output = stdout.readlines()
    aggr_usage=0
    for i in output:
        try:
            aggr_usage=int(i.split("%")[0].split(" ")[])
        except:
            aggr_usage=0
        if aggr_usage>85:
            print("High usage aggregate:\n")
            print(i)

    #ifgrp show
    stdin, stdout, stderr = ssh_client.exec_command("ifgrp show")
    output = stdout.readlines()
    ifgrp_status=True
    for i in output:
        for t in errors:
            if t in i.split(" "):
                print(f"ifgrp is {t}:")
                print(i)
                ifgrp_status=False

    if ifgrp_status==True:
        print("All ifgrps are OK.\n")

    #check if takeover is possible
    stdin, stdout, stderr = ssh_client.exec_command("storage failover show")
    output = stdout.readlines()
    for i in output:
        try:
            for j in i.split(" "):
                if "false" in j:
                    print("takeover unavailable:\n")
                    print (i)
        except:
            None

    #environment status
    stdin, stdout, stderr = ssh_client.exec_command("system node run ode * ommand environment status")
    output = stdout.readlines()
    environment_errors=re.findall(r"\W*(error: [1])\W*", str(output))
    if environment_errors != []:
        print("There are environment status problems! Please check them manually.\n")
    else:
        print("Environment status OK.\n")

    #storage shelf show
    stdin, stdout, stderr = ssh_client.exec_command("storage shelf show")
    output = stdout.readlines()
    shelf_status=True
    for i in output:
        for t in errors:
            if t in i.split("\r\n")[0].split(" ")[]:
                print("Shelf has a problem:\n")
                print(i)
                shelf_status=False
    if shelf_status==True:
        print("All shelves are OK.\n")

    #sp show
    stdin, stdout, stderr = ssh_client.exec_command("sp show")
    output = stdout.readlines()

    sp_status=True
    for i in output:
        for t in errors:
            if t in i.split(" "):
                print(f"sp is {t}:")
                print(i)
                sp_status=False

    if sp_status==True:
        print("SP is online. Testing availability...\n")

    # ssh sp
    sp_list=re.findall(r"(?:[0]{1,3}\.){3}[0]{1,3}", str(output))
    ssh_client.close()

    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=sp_list[0], username='Readrix', password='txyrydh440!')
        print(f"Connection to sp {sp_list[0]} success!\n")

    except:
        try:
            print(f"connection to sp {sp_list[0]} failed\n")
        except:
            print("his netapp has ONTAP DEPLOY. Please check it manually.\n")
    ssh_client.close()
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=sp_list[1], username='Readrix', password='txyrydh440!')
        print(f"Connection to sp {sp_list[1]} success!\n")

    except:
        try:
            print(f"connection to sp {sp_list[1]} failed\n")
        except:
            print("his netapp has ONTAP DEPLOY. Please check it manually.\n")
    ssh_client.close()
    



