from scapy.all import *

def processpacket(p):

    if ("GET" in str(p)) or ("POST" in str(p)):

         direction =  p.sprintf("{IP:%IP.src% -> %IP.dst%\n}")
         packetinfo = p.sprintf("{Raw:%Raw.load%}").split(r"\r\n")
         print(direction)
         for r in packetinfo:
            print(r)
         print ("***************************************************")


if __name__== "__main__" : 

    ##Following Lines is command to start capturing Packets

    #Windows Hotspot Packet Capture
    #sniff(iface="Microsoft Wi-Fi Direct Virtual Adapter #2", filter="tcp port 80", prn=processpacket)

    #Linux Packet Capture (not tested)
    #sniff(iface="wlan0", filter="tcp port 80", prn=processpacket)


    #Localhost Packet Capture ( RESULTS OBTAINED WERE DIFFERENT FROM WINDOWS HOTSPOT?)
    sniff( filter="tcp port 80", prn=processpacket)
