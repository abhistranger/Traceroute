import socket
import random
import time
import sys
from scapy.all import *
import matplotlib.pyplot as plt

#Icmp_code = socket.getprotobyname('icpm')


if(len(sys.argv)) <= 1:
    # no domain name provided
    print("No domain name provided")
    sys.exit(1)

domain_name = sys.argv[1]
ip_add = None
try:
    ip_add = socket.gethostbyname(domain_name)
except socket.gaierror:
    # wrong domain name
    print(f'Invalid domain name: ', end='')
    print(domain_name)
    sys.exit(1)
except:
    print("Wrong")
    sys.exit(1)

max_hops = 30
RTT_list = []
hop_list = [j for j in range(1, max_hops+1)]

for i in range(1, max_hops+1):
    # create packet
    packet = IP(dst=ip_add, ttl=i, id=RandShort())

    ts = time.time()
    # send and get reply back
    reply = sr1(packet/ICMP(), retry=1, timeout=3, verbose=0)
    te = time.time()

    if reply:
        RTT_list += [(te-ts)*1000, ]
        print('{:2} {:8.3f} ms    '.format(i, (te-ts)*1000), end='')
        print(reply.src)
        if reply and reply.src == ip_add:
            # Reached destination
            print("Done routing!",)
            break
    else:
        # No reply
        RTT_list += [0]
        print("{:2}     *          ".format(i), end='')
        print("Request timed out.")

plt.figure(figsize=(12, 6))
plt.plot(hop_list, RTT_list, alpha=0.8, linewidth=2, marker='o')
plt.xlabel('Hop Number')
plt.ylabel('RTT (ms)')
plt.legend()
plt.savefig('a1.png')
