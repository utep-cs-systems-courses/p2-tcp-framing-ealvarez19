#! /usr/bin/env python3
#! /usr/bin/env python3
# Echo server program

import socket, sys, re
sys.path.append("../lib")       # for params
import params
from framedSock import framedSock
import os
switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

while 1:
    conn, addr = s.accept()  # wait until incoming connection request (and accept it)
    print('Connected by', addr)
    framedSock = framedSock(conn)

    if os.fork() == 0:                         #child
        message = (framedSock.rcvMessage())
        filename = message

        if os.path.isfile(filename):           #if file already exists
            framedSock.sndMessage(b"No")       #send No
            conn.shutdown(socket.SHUT_WR)
        else:
            framedSock.sndMessage(b"OK")               #send OK if file no exits
            
        fd = os.open(filename,os.O_CREAT | os.O_WRONLY)#open file
        os.write(fd,framedSock.rcvMessage().encode())#write into file
        os.close(fd)
            






