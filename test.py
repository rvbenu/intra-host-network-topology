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


"""
Return PCI description given an ID. 
First, query /usr/share/misc/pci.ids (maybe /usr/local/share/pci.ids)
If not found, query online database /usr/local/share/pci.ids
"""
def get_pci_description(vendor_id, device_id):
    offline_command = 
    # Run
    online_command = 
    # Run

def get_pci_descriptions(pci_ids):
    
def main():

if __name__ = '__main__':
    main()
