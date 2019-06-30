#!/usr/bin/python3

'''
AUTHOR: Annette
PROGRAM DESC: ARP Ping for live devices with Scapy


EXAMPLE MACVENDORS OUTPUT

{'result': {'address': '1 Infinite Loop,Cupertino  CA  95014,US',
            'company': 'Apple, Inc.',
            'country': 'US',
            'end_hex': '749EAFFFFFFF',
            'mac_prefix': '74:9E:AF',
            'start_hex': '749EAF000000',
            'type': 'MA-L'}}

'''


from netaddr import IPAddress, IPNetwork
from scapy.all import arping, conf
import requests

'''
Return: Gateway ip address from 0.0.0.0 network address 
and network mask entry in routing table

E.g.

Network          Netmask          Gateway        
0.0.0.0          0.0.0.0          192.168.1.254
'''
def get_gateway_ip():
        #Ref: Scapy Routing Table
        conf.route.resync()
        routes = conf.route.routes
        for route in routes:
                if route[0] == 0 and route[1] == 0:
                        return route[2]

'''
Return: List of subnets (CIDR) from routing table where gateway ip is in
'''
def get_subnets():
        
        #Ref: IOT Inspector utils.py
        gateway_ip = get_gateway_ip()
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
Input: List of subnets (CIDR) from routing table where gateway ip is in 
Return: List of live hosts found within each subnet after arp ping
'''
def scan_devices(subnet_set):

        ans_lists = set()

        for subnet in subnet_set:
                ans,unans = arping(str(subnet))
                ans_lists.add(ans)
                
        return ans_lists

'''
Input: Device Mac Address
Return: Device's Vendor Name
'''
def mac_lookup(mac):

        MAC_URL = 'http://macvendors.co/api/%s'
        result = requests.get(MAC_URL % mac).json()
        return result['result']['company']

'''
Input: List of live hosts found within each subnet after arp ping
Output: List of devices (IP Address, Mac Address, Vendor)
'''
def save_devices(ans_lists):

        for ans in ans_lists:
                for dev in ans: 
                        
                        company = mac_lookup(dev[1].src)
                        print(dev[1].psrc, dev[1].src, company)

        

if__name__== "__main__":
      
        #Get list of subnets gateway is in (CIDR)
        ##TODO: Return value for Empty Gateway Values/Empty subnet_set
        subnet_set = get_subnets()
        #Scan for Live Hosts
        ans_lists = scan_devices(subnet_set)
        #Func: Lookup Vendor name + Update users' database
        save_devices(ans_lists)


