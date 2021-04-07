class framedSock:
    
    def __init__(self,Socket): #receive connected socket
        self.connectedSocket = Socket
        self.data = "" #buffer

    def sndMessage(self,message):              #send message
        length = str(len(message)) + ':'       #this is the frame
        lengthBytes = bytearray(length,'utf-8')#convert length to bytes
        message = lengthBytes + message        #concat length and message
        self.connectedSocket.send(message)

    def rcvMessage(self):
        message = ""
        if self.data == "":
            self.data += self.connectedSocket.recv(100).decode()#receive 100 bytes of data 
            firstDataIndex , lastDataIndex = separate(self.data)      #first and last index of data
            message += self.data[firstDataIndex:lastDataIndex]      #adding first packet to message
            self.data = self.data[lastDataIndex:]                      #start from lastData sent
        
        while self.data: #while there is data to be sent
            firstDataIndex , lastDataIndex = separate(self.data)
            if len(data) < lastDataIndex:                #if all data can be read and there is more
                self.data += self.connectedSocket.recv(100).decode()
            else:
                message +=data[firstDataIndex:lastDataIndex]
                self.data = self.data[lastDataIndex:]
            
        return message

def separate(data):#receives string of data
    num=""

    while(data[0].isdigit()):
        num+=data[0]
        data = data[1:]       #next character

    if num.isnumeric():                         
        firstDataIndex = len(num)+1              #first index of data after length
        lastDataIndex = int(num) + (len(num)+1)  #last data index
        return firstDataIndex, lastDataIndex
    else:
        return None








    
    


        

        
        
