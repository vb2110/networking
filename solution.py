from socket import *
import os
import sys
import struct
import time
import select
import binascii
from statistics import stdev

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 1

class RTT_Data:
    pktsSent = 0
    pktsRcvd = 0
    minTime = 999999999
    maxTime = 0
    totTime = 0

rttdata = RTT_Data

# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise

def checksum(string):
# In this function we make the checksum of our packet
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = (string[count + 1]) * 256 + (string[count])
        csum += thisVal
        csum &= 0xffffffff
        count += 2

    if countTo < len(string):
        csum += (string[len(string) - 1])
        csum &= 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


#def build_packet():
    #Fill in start
    # In the sendOnePing() method of the ICMP Ping exercise ,firstly the header of our
    # packet to be sent was made, secondly the checksum was appended to the header and
    # then finally the complete packet was sent to the destination.

    # Make the header in a similar way to the ping exercise.
    # Append checksum to the header.

    # Don’t send the packet yet , just return the final packet in this function.
    #Fill in end

    # So the function ending should look like this

 #   packet = header + data
 #  return packet


def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout
    global rttdata

    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []:  # Timeout
            return "Request timed out."

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)

        # Fill in start

        # Fetch the ICMP header from the IP packet
        rttdata.pktsRcvd += 1
        icmp = recPacket[20:28]
        icmpType, icmpCode, icmpChecksum, icmpPacketID, icmpSeqNumber = struct.unpack('bbHHh', icmp)
        if icmpPacketID == ID:
            bytesInDouble = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
            return timeReceived - timeSent

        # Fill in end
        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request timed out."


def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)

    myChecksum = 0
    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network  byte order
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str

    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object.

def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")
    global rttdata

    # SOCK_RAW is a powerful socket type. For more details:   http://sockraw.org/papers/sock_raw
    mySocket = socket(AF_INET, SOCK_RAW, icmp)
    myID = os.getpid() & 0xFFFF  # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    rttdata.pktsSent += 1
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return delay

def ping(host, timeout=1):
    # timeout=1 means: If one second goes by without a reply from the server,  	# the client assumes that either the client's ping or the server's pong is lost
    
    global rttdata
    dest = gethostbyname(host)
    print("Pinging " + dest + " using Python:")
    print("")
    # Calculate vars values and return them
    #  vars = 
    # Send ping requests to a server separated by approximately one second
    stdevDelay = []

    for i in range(0, 4):
        delay = doOnePing(dest, timeout)
        if delay == "Request timed out.":
            print(delay)
        else:
            delay = delay * 1000
            stdevDelay.append(delay)
            print(delay)
        time.sleep(1)  # one second

        if delay != "Request timed out.":
            if rttdata.minTime > delay:
                rttdata.minTime = delay
            if rttdata.maxTime < delay:
                rttdata.maxTime = delay
            rttdata.totTime += delay

    if rttdata.pktsRcvd == 0:
        packet_recv = rttdata.pktsRcvd
        packet_sent = rttdata.pktsSent
        packet_loss = 100
        packet_min = 0
        packet_max = 0
        packet_avg = 0.0
        stdev_var = (0, 0)

        vars = [str(round(packet_min, 2)), str(round(packet_avg, 2)), str(round(packet_max, 2)), str(round(stdev(stdev_var), 2))]
        print("\n----%s PING Statistics----" % dest)
        print(str(packet_sent) + " packets transmitted, " + str(packet_recv) + " packets received, " + str(packet_loss) + "% packet loss")
        print("round-trip min/avg/max/stddev", vars)
        return vars
        
    else:
        packet_recv = rttdata.pktsRcvd
        packet_sent = rttdata.pktsSent
        packet_min = rttdata.minTime
        packet_avg = rttdata.totTime / rttdata.pktsRcvd
        packet_max = rttdata.maxTime
        packet_loss = (rttdata.pktsSent - rttdata.pktsRcvd) / rttdata.pktsSent
        stdev_var = stdevDelay

        vars = [str(round(packet_min, 2)), str(round(packet_avg, 2)), str(round(packet_max, 2)), str(round(stdev(stdev_var), 2))]
        print("\n----%s PING Statistics----" % dest)
        print(str(packet_sent) + " packets transmitted, " + str(packet_recv) + " packets received, " + str(packet_loss) + "% packet loss")
        print("round-trip min/avg/max/stddev = ", vars)
        return vars

if __name__ == '__main__':
    ping("google.co.il")
