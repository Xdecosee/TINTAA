'''
AUTHOR: Annette
PROGRAM DESC: Identify Module for device discovery

TODO (Add on):
Feature 1 - Return value for Empty Set values
Feature 2 - Decide on background thread for device identification
Feature 3 - Class files for devices and packets to access values more easily
'''

from netaddr import IPAddress, IPNetwork
from scapy.all import arping, conf
import requests


'''
Return: Gateway ip address from default route 0.0.0.0/0
and network mask entry in routing table

E.g.

Network          Netmask          Gateway        
0.0.0.0          0.0.0.0          192.168.1.254
'''
def get_gateway():
        #Ref: Scapy Routing Table
        conf.route.resync()
        routes = conf.route.routes
        for route in routes:
                if route[0] == 0 and route[1] == 0:
                        return route[2]


'''
Input: Gateway Ip Address
Return: Set of subnets (CIDR) from routing table where gateway ip is in
'''
def get_subnets():
        
        #Ref: IOT Inspector utils.py
        gateway_ip = get_gateway()
        subnet_set = set()

        if gateway_ip:

                routes = conf.route.routes
                for route in routes:

                        network, netmask, gateway = route[0], route[1], route[2]

                        if gateway != '0.0.0.0' or not netmask or not network :
                                continue

                        network = IPAddress(network)
                        net_cidr = IPAddress(netmask).netmask_bits()
                        subnet = IPNetwork("{}/{}".format(network, net_cidr))

                        if gateway_ip in subnet:
                                subnet_set.add(subnet)
                                return subnet_set



'''
Input: Device Mac Address
Return: Device's Vendor Name
'''
def mac_lookup(mac):

        MAC_URL = 'http://macvendors.co/api/%s'
        result = requests.get(MAC_URL % mac).json()
        return result['result']['company']


'''
Input: Set of subnets (CIDR) from routing table where gateway ip is in 
Return: Set of live hosts & their vendor (tuple) found within each subnet after arp ping
'''
def scan_devices(subnet_set):

        ans_lists = set()
        dev_list = set()

        for subnet in subnet_set:
                ans,unans = arping(str(subnet))
                ans_lists.add(ans)

        for ans in ans_lists:
                for dev in ans: 
                        company = mac_lookup(dev[1].src)
                        new_dev = (dev[1].psrc, dev[1].src, company)
                        dev_list.add(new_dev)
                
        return dev_list



    

