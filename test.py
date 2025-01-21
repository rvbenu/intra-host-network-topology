import subprocess


# Returns a list containing PCI IDs found in the server. 
def get_pci_ids():
    command = "grep PCI_ID /sys/bus/pci/devices/*/uevent | cut -d'=' -f2"
    try:
        result = subprocess.run(
            command, shell=True, text=True, capture_output=True, check=True
        )
        pci_ids = result.stdout.strip().split("\n")
        return pci_ids
    except subprocess.CalledProcessError as e:
        print(f"Error fetching PCI IDs: {e.stderr}")
        return []

def parse_pci_description(output):
    i = output.find("SDevice:")
    i += 8
    device = ""
    c = output[i]
    while(c != "\n"):
       device += c
       i += 1
       c = output[i]
    return output


"""
Return PCI description given a PCI ID. 
    Query locally first. If not found, query central PCI ID database. 
    Returns value corresponding to tag SDevice (if found). Returns 'Not found'
    otherwise. 
"""
def get_pci_description(vendor_id, device_id):
    pci_id = f"{vendor_id}:{device_id}"

    """ 
    It is recommendable to query the central PCI ID database 
    to avoid overloading the database servers. 
    """
    offline_command = f"lspci -vmm -d {pci_id}"
    offline_output = subprocess.run(
            offline_command, shell=True, text=True, capture_output=True, check=True
        )
    # Check that output returned something. If so, parse it.  

    online_command = 
    # Run

def get_pci_descriptions(pci_ids):
    
def main():

if __name__ = '__main__':
    main()
