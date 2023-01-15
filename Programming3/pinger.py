import os
import sys
import struct
import time
import select
from socket import *
import binascii

ICMP_ECHO_REQUEST = 8


def checksum(string):
    csum = 0
    countTo = (len(string) / 2) * 2

    count = 0
    while count < countTo:
        thisVal = string[count + 1] * 256 + string[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2

    if countTo < len(string):
        csum = csum + ord(string[len(str) - 1])
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def receiveOnePing(mySocket, ID, timeout, destAddr):
    global rtt_min, rtt_max, rtt_sum, rtt_cnt
    timeLeft = timeout
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
        type, code, checksum, head_ID, sequnce = struct.unpack(
            'bbHHh', recPacket[20:28])
        if type != 0:
            return 'unavailabe type'
        if code != 0:
            return 'unavailabe code'

        ip_header = struct.unpack('!BBHHHBBH4s4s', recPacket[:20])
        send,  = struct.unpack('d', recPacket[28:])
        ip = ip_header[8]
        source = inet_ntoa(ip)
        roundTrip = (timeReceived - send)
        rtt = roundTrip * 1000
        rtt_min = min(rtt, rtt_min)
        rtt_max = max(rtt, rtt_max)
        rtt_sum = rtt_sum + rtt
        rtt_cnt = rtt_cnt + 1

        return '{} bytes from {}; time={:.1f} ms'.format(len(recPacket), source, rtt)
        # Fill in end

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request timed out."


def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)

    myChecksum = 0
    # Make a dummy header with a 0 checksum.
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        myChecksum = htons(myChecksum) & 0xffff
        # Convert 16-bit integers from host to network byte order.
    else:
        myChecksum = socket.htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data

    # AF_INET address must be tuple, not str
    mySocket.sendto(packet, (destAddr, 1))
    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object


def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")

    # Fill in start
    # Create Socket here
    mySocket = socket(AF_INET, SOCK_DGRAM, icmp)
    # Fill in end

    myID = os.getpid() & 0xFFFF  # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return delay


def ping(host, timeout=1):
    global rtt_min, rtt_max, rtt_sum, rtt_cnt
    rtt_min = float('+inf')
    rtt_max = float('-inf')
    rtt_sum = 0
    rtt_cnt = 0
    cnt = 0
    # timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the client's ping or the server's pong is lost
    dest = gethostbyname(host)
    print("Pinging " + host + " using Python:")
    # Send ping requests to a server separated by approximately one second
    try:
        while 1:
            cnt = cnt + 1
            print(doOnePing(dest, timeout))
            time.sleep(1)
    except KeyboardInterrupt:

        #Fill in start
        if cnt != 0:
            print('--- {} ping statistics ---'.format(host))
            if rtt_cnt != 0:
                rtt_avg = rtt_sum / rtt_cnt
                print(
                    'round-trip min/avg/max {:.3f}/{:.3f}/{:.3f} ms'.format(rtt_min, rtt_avg, rtt_max))
        #Fill in end


if __name__ == '__main__':
    try:
        address = input("Enter the address!:")
        ping(address)
    except Exception:
        print("Wrong input!")
