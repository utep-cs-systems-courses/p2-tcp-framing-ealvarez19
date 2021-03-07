#! /usr/bin/env python3

import sys, re,time
from socket import *

serverSocket = socket(AF_INET,SOCK_STREAM) #IPV4 and TCP connection
serverSocket.bind(('127.0.0.1',50000))     #bind host and port
serverSocket.listen(100)                      #Listening in port 50000

clientSocket, addr = serverSocket.accept() #accept connection
time.sleep(10)                             #Sleep to get all the message
print("Received a connection from: ", addr)
message = clientSocket.recv(1024)          #get file from client

print("Message: ", message.decode())

remoteFile = open("file2.txt","w+")        #create remote file in server
remoteFile.write(message.decode());        #write into remote file
remoteFile.close()                         #close file







