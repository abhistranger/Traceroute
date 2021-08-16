import socket
import random
import time
import sys
from scapy.all import *

#Icmp_code = socket.getprotobyname('icpm')


if(len(sys.argv)) <= 1:
    print("No domain name provided")
    sys.exit(1)

domain_name = sys.argv[1]
ip_add = None
try:
    ip_add = socket.gethostbyname(domain_name)
except socket.gaierror:
    print(f'Invalid domain name: ', end='')
    #print("Unable to resolve target system name ", end='')
    print(domain_name)
    sys.exit(1)
except:
    print("Wrong")
    sys.exit(1)

max_hops = 30

for i in range(1, 31):
    packet = IP(dst=ip_add, ttl=i, id=RandShort())

    ts = time.time()
    reply = sr1(packet/ICMP(), retry=1, timeout=3, verbose=0)
    te = time.time()

    if reply:
        if reply and reply.src == ip_add:
            # Reached destination
            print("Done!", reply.src)
            break
        #print("%d hops away: " % i, reply.src)
        print('{:2} {:8.3f} ms    '.format(i, (te-ts)*1000), end='')
        print(reply.src)
    else:
        # No reply
        #print('{:2} {:8.3f} ms    '.format(i, (te-ts)*1000), end='')
        print("{:2}     *          ".format(i), end='')
        print("Request timed out.")
