import socket
import time
import sys
from scapy.all import *
import matplotlib.pyplot as plt

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
if(len(sys.argv)) == 3:
    max_hops = int(sys.argv[2])
RTT_list = []
hop_used = 0
done = False

print("Tracing route to "+domain_name+" ["+ip_add+"]")
print("maximum hopes of "+str(max_hops)+":")

for i in range(1, max_hops+1):
    # create packet
    packet = IP(dst=ip_add, ttl=i)

    '''ts = time.time()
    # send and get reply back
    reply = sr1(packet/ICMP(), retry=1, timeout=3, verbose=0)
    te = time.time()
    RTT=(te-ts)*1000'''

    RTT = -1
    reply = None
    for k in range(3):
        t_s = time.time()
        # send and get reply back
        reply_ = sr1(packet/ICMP(), retry=1, timeout=1, verbose=0)
        t_e = time.time()
        if(RTT == -1 or ((t_e-t_s)*1000 < RTT and reply_ and reply and reply_.src == reply.src)):
            reply = reply_
            RTT = (t_e-t_s)*1000

    hop_used = i
    if reply:
        RTT_list += [RTT, ]
        print('{:2} {:8.3f} ms    '.format(i, RTT), end='')
        print(reply.src)
        if reply and reply.src == ip_add:
            # Reached destination
            print("Trace Complete!",)
            done = True
            break
    else:
        # No reply
        RTT_list += [0]
        print("{:2}     *          ".format(i), end='')
        print("Request timed out.")

if(done == False):
    print("Trace Incomplete due to hop limit exceeded or some other reasons")
if done:
    hop_list = [j for j in range(1, hop_used+1)]
    plt.figure(figsize=(12, 8))
    plt.plot(hop_list, RTT_list, alpha=0.8, linewidth=2, marker='o')
    plt.xlabel('Hop Number')
    plt.ylabel('RTT (ms)')
    ax = plt.gca()
    ax.set_xticks(hop_list)
    ax.set_xticklabels(hop_list)
    plt.savefig('a1_'+domain_name+'.png')
