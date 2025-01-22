import subprocess


# Return list containing PCI IDs found in the server. 
def get_pci_ids():
    command = "grep PCI_ID /sys/bus/pci/devices/*/uevent | cut -d'=' -f2"
    try:
        process = subprocess.run(
                command, shell=True, text=True, capture_output=True, check=True
            )
        pci_ids = process.stdout.strip().split("\n")
        return pci_ids
    except subprocess.CalledProcessError as e:
        print(f"Error fetching PCI IDs: {e.stderr}")
        return []

def parse_pci_device_name(stdout):
    device_name = ""
    
    index_begin = index_end = stdout.find("SDevice:")
    index_begin += 8
    c = stdout[index_end]
    while(c != "\n"):
        index_end += 1
        c = stdout[index_end]

    return stdout[index_begin:index_end]


"""
Return PCI description given a PCI ID. 
    Query locally first. If not found, query central PCI ID database. 
    Returns value corresponding to tag SDevice (if found). Returns 'Not found'
    otherwise. 
"""
def get_pci_device_name(vendor_id, device_id):
    pci_id = f"{vendor_id}:{device_id}"

    """ 
    It is recommendable to query the local PCI ID database first 
    to avoid overloading the central PCI ID database servers. 
    """

    command_query_local = f"lspci -vmm -d {pci_id}"
    command_query_central = f"lspci -q -vmm -d {pci_id}"
    
    try: 
        process_query_local = subprocess.run(
                command_query_local, shell=True, text=True, capture_output=True, check=True
            )
        if not process_query_local.stdout:
            print(f"{pci_id} not found in local database. \n")
        else: 
            device_name = parse_pci_device_name(process_query_local.stdout)
            return f"{pci_id}: {device_name}"
    except subprocess.CalledProcessError as e:
        print(f"Error querying local database: {e.stderr} \n")
 
    try: 
        process_query_central = subprocess.run(
                command_query_central, shell=True, text=True, capture_output=True, check=True
            )
        if not process_query_central.stdout:
            print(f"{pci_id} not found in central database. \n")
        else:
            device_name = parse_pci_device_name(process_query_central.stdout)
            return f"{pci_id}: {device_name}"
    except subprocess.CalledProcessError as e:
        print(f"Error querying central database: {e.stderr} \n")
   


    return f"{pci_id} not found. \n"




def main():
    pci_ids = get_pci_ids()
    for pci_id in pci_ids:
        vendor_id = pci_id[0:4]
        device_id = pci_id[5:9]
        device_name = get_pci_device_name(vendor_id, device_id)
        print(f"{device_name} \n")



if __name__ == '__main__':
    main()
