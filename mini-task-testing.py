import subprocess


"""
get_pci_ids
    Returns a list of IDs of PCIs found in the server. 
"""
def get_pci_ids():
    command = "grep PCI_ID /sys/bus/pci/devices/*/uevent | cut -d'=' -f2"
    try:
        process_stdout = subprocess.check_output(
                command, text=True, shell=True
            )
        pci_ids = process_stdout.strip().split("\n")
        return pci_ids
    except subprocess.CalledProcessError as e:
        print(f"Error fetching PCI IDs: {e}")
        return []


"""
parse_pci_info
    Returns the PCI vendor and device name as a string separated by a tab. 
    'stdout' corresponds to an 'lspci -vmm -d <pci_id>' call. 
"""
def parse_pci_info(stdout):
    
    pci_info = {}
    stdout_lines = stdout.splitlines()

    for line in stdout_lines:
        if "\t" in line: 
            # The tag and the value are separated by a single tab character.  
            tag_value_pair = line.split("\t", 1)
            tag, value = tag_value_pair
            # Remove unnecessary white space
            tag = tag.rstrip(":").strip()
            value = value.strip()

            pci_info[tag] = value

    pci_vendor = pci_info.get("Vendor", "Not found")
    pci_device = pci_info.get("Device", "Not found")

    return f"Vendor: {pci_vendor}, \t Device: {pci_device}"


"""
get_pci_device_name
    Returns the vendor and device name of a PCI given its vendor and device ID. 
    Queries locally first. If not found, queries central PCI ID database. 
    It is recommendable to query the local PCI ID database first 
    to avoid overloading the central PCI ID database servers. 
    If PCI not found, returns "Not found"
"""
def get_pci_info(vendor_id, device_id):
    pci_id = f"{vendor_id}:{device_id}"
    
    command_query_local = f"lspci -vmm -d {pci_id}"
    command_query_central = f"lspci -q -vmm -d {pci_id}"
    
    try: 
        process_query_local_stdout = subprocess.check_output(
                command_query_local, text=True, shell=True
            )
        if not process_query_local_stdout:
            print(f"{pci_id} not found in local database. \n")
        else: 
            pci_info = parse_pci_info(process_query_local_stdout)
            return f"{pci_id}: {pci_info}"
    except subprocess.CalledProcessError as e:
        print(f"Error querying local database: {e} \n")

    try: 
        process_query_central_stdout = subprocess.check_output(
                command_query_central, text=True, shell=True    
            )
        if not process_query_central_stdout:
            print(f"{pci_id} not found in central database. \n")
        else:
            pci_info = parse_pci_info(process_query_central_stdout)
            return f"{pci_id}: {pci_info}"
    except subprocess.CalledProcessError as e:
        print(f"Error querying central database: {e} \n")
   
    return f"{pci_id} not found. \n"


def main():
    pci_ids = get_pci_ids()
    for pci_id in pci_ids:
        vendor_id = pci_id[0:4]
        device_id = pci_id[5:9]
        pci_info = get_pci_info(vendor_id, device_id)
        print(f"{pci_info} \n")


if __name__ == '__main__':
    main()
