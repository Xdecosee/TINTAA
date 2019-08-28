from scapy.all import *

packets = []

def processpacket(p):

    if ("GET" in str(p)) or ("POST" in str(p)):

         src =  p.sprintf("{IP:%IP.src%}")
         dst = p.sprintf("IP:%IP.dst%}")
         packetinfo = p.sprintf("{Raw:%Raw.load%}").split(r"\r\n")
         entry = (src, dst, packetinfo)
         packets.append(entry)
         #print(direction)
         #for r in packetinfo:
            #print(r)
       #  print ("***************************************************")


def startcapture():
   sniff( filter="tcp port 80", prn=processpacket, count=10)
   return packets


##Following Lines is command to start capturing Packets

#Windows Hotspot Packet Capture
#sniff(iface="Microsoft Wi-Fi Direct Virtual Adapter #2", filter="tcp port 80", prn=processpacket, count = 100000)

#Linux Packet Capture (not tested)
#sniff(iface="wlan0", filter="tcp port 80", prn=processpacket)

#Localhost Packet Capture ( RESULTS OBTAINED WERE DIFFERENT FROM WINDOWS HOTSPOT?)
# #sniff( filter="tcp port 80", prn=processpacket)
