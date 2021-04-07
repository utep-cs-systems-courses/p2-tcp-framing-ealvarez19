#! /usr/bin/env python3

# Echo client program
import socket, sys, re, time,os
sys.path.append("../lib")       # for params
import params
from myReadLine import myReadLine
from myReadLine import parseTCPInput
from framedSock import framedSock

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--delay'), 'delay', "0"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage  = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

delay = float(paramMap['delay']) # delay before reading (default = 0s)
if delay != 0:
    print(f"sleeping for {delay}s")
    time.sleep(delay)
    print("done sleeping")

framedSocket = framedSock(s)

input = myReadLine() #input from user

command, localFile, remoteFile = parseTCPInput(input) #parse input from user

print("Sending Remote File...")
framedSocket.sndMessage(remoteFile.encode())

serverReply = framedSocket.rcvMessage()
print("Server response: ",serverReply)

if serverReply == "OK":
    fd = os.open(localFile,os.O_RDONLY) #open local file to be sent
    buffer = ""
    message = ""
    
    
    while 1:
        buffer = os.read(fd,100)             #read 100 bytes
        data = buffer.decode()               #data string
        if len(data) == 0:                   #if there is no more data then exit
            break
        message +=data                       #otherwise append to message
    framedSocket.sndMessage(message.encode())#send message
    s.close()                                #close socket
else:
    os.write(2,("Error").encode())           #if the file already exists then print error
    sys.exit(1)

    
            

    
