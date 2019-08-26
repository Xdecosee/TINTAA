#!/usr/bin/python3

'''
AUTHOR: Annette
PROGRAM DESC: Scan and save live devices on predefined subnet address (CIDR) => hardcode value in 'input' variable
'''

import identify

if __name__== "__main__" : 
      
        #[Hardcode]
        #input = "192.168.1.0/24"
        input = "192.168.4.1/24"
        #Scan for Live Hosts => [Invoke from frontend]
        dev_list = identify.scan_devices(input)
        #Func: Lookup Vendor name + [Update users' database]
        for dev in dev_list :
                print(dev)
       


