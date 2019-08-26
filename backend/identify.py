'''
AUTHOR: Annette
PROGRAM DESC: Identify Module for device discovery
'''
from scapy.all import arping
import requests

'''
Input: Device Mac Address
Return: Device's Vendor Name
'''
def mac_lookup(mac):

        MAC_URL = 'http://macvendors.co/api/%s'
        result = requests.get(MAC_URL % mac).json()
        return result['result']['company']


'''
Input: Pre-setup/Pre-defined subnet address in CIDR form (hardcoded)
Return: Set of live hosts & their vendor (tuple) found within subnet after arp ping
'''
def scan_devices(subnet_addr):

        dev_list = set()
        ans,unans = arping(subnet_addr)

        for dev in ans: 
                company = mac_lookup(dev[1].src)
                new_dev = (dev[1].psrc, dev[1].src, company)
                dev_list.add(new_dev)
                
        return dev_list



    

