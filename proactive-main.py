import proactive

ip_dict = {"ssh_dns_name_of_netapp":"netapp_ssh_address"}


if __name__ == "__main__":
    for i,t in ip_dict.items():
        proactive.proactive(i,t)
    print("PROACTIVE FINISHED-")
