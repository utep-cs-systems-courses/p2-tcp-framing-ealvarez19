import framedSock
import sys, os, socket, threading
import myReadLine
from threading import Thread
from time import time

threadNum = 0
fileSet = set()                 #set of files that are busy
lock = threading.Lock()

class Worker(Thread):
    def __init__(self,conn,addr):
        global threadNum
        Thread.__init__(self, name="Thread-%d" % threadNum)
        threadNum += 1
        self.conn = conn
        self.addr = addr

    def checkTransfer(self,fileName):
        global fileSet
        global lock
        lock.acquire()                      #acquire lock to check if file is being transfered

        if fileName in fileSet:
            availability = False
        else:
            availability = True
            fileSet.add(fileName)
        lock.release()                      #release lock to be able for another request
        return availability

    def start(self):
        framedSock = framedSock.framedSock(self.conn)     #framed socket

        fileName = framedSock.rcvMessage()                #receive file name
        availability = self.checkTransfer(fileName)       #check if file is being transfered

        if availability  == False:                        #if it is busy, wait
            framedSock.sndMessage(b"wait")
        elif os.path.isfile(fileName):                    #if file already exists, send error
            fs.sndMessage("No")
        else:
            framedSock.sndMessage(b"OK")                 #if file is available
            try:
                fd = os.open(fileName, os.O_CREAT | os.O_WRONGLY) #open file and write into it
                os.write(fd, framedSock.rcvMessage().encode())
                os.close(fd)

            except:
                framedSock.sndMessage(b"Error writing into file")
        self.conn.shutdown(socket.SHUT_WR)

    def end(self,fileName): #removes file from set
        global fileSet
        fileSet.remove(fileName)
                                                
