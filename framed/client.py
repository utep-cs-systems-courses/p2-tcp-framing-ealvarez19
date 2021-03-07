#! /usr/bin/env python3

import sys, re
from socket import *

if len(sys.argv) > 0: #if client.py has arguments
    localFile = sys.argv[1] #name of local file to be sent
    host , remoteFile = sys.argv[2].split(':')
serverPort = 50000

clientSock = socket(AF_INET,SOCK_STREAM) # IPV4 and TCP connection
clientSock.connect((host,serverPort))  # make a connetion with server
packet = [] #packets list
textFile = open(localFile,"rb") #open the file that is passed as argument
while True:
    data = textFile.read(7)     #read 7 bytes from file
    if not data:
        break
    packet.append(data)         #next 7 bytes in the packets list

while len(packet)!=0:           #while there is a packet
    clientSock.send(packet[0])  #send the packet
    packet = packet[1:]         #next packet in packet list




    



