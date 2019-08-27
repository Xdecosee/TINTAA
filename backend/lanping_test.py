#!/usr/bin/python3

'''
AUTHOR: Annette
PROGRAM DESC: Scan and save live devices
'''

import identify

if __name__== "__main__" : 
      
        #Get list of subnets gateway is in (CIDR)
        subnet_set = identify.get_subnets()
        #Scan for Live Hosts
        dev_list = identify.scan_devices(subnet_set)
        #Func: Lookup Vendor name + Update users' database
        for dev in dev_list :
                print(dev)
       


