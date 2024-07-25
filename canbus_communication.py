import can
import threading
import time

class Channel:
    CanC = 0
    CanB = 1

class WriteMessage:
    def __init__(self, pid:int, message:list, times:int):
        self.pid     = pid
        self.message = message
        self.times   = times

class ReadMessage:
    def __init__(self, pid:int, offset:int, len:int, alias:str):
        self.alias  = alias
        self.pid    = pid
        self.offset = offset
        self.len    = len
        self.value  = 0

class MBcanbus:
    def __init__(self, channel:int):
        self.Canbus = can.interface.Bus(channel=f'can{channel}', bustype='socketcan')
        self.listOfMessagesToSend = [] 
        self.listOfMessagesToRead = [] 

    def AddCheckList(self, pid:int, offset:int, len:int, alias:str):
        self.listOfMessagesToRead.append( ReadMessage(pid, offset, len, alias) )

    def SendMessage(self, pid:int, message:list, times:int):
        self.listOfMessagesToSend.append( WriteMessage(pid,message,times) )

    def MessageSender(self):
        while True:
            i=0
            while i < len(self.listOfMessagesToSend):
                # get message object
                msg = self.listOfMessagesToSend[i]

                # check are permanent message
                if msg.times != -1:
                    msg.times -= 1

                # send message to canbus
                self.Canbus.send(can.Message(arbitration_id=msg.pid, data=msg.message, is_extended_id=False))

                # if delete index, not need move index
                if(msg.times == 0):
                    self.listOfMessagesToSend.pop(i)
                else:
                    i+=1
            time.sleep(1)

    def GetValueByCanMsg(msg:list, offset:int, length:int):
        returnStr = ""
        for i in msg:
            # Convert every index to 00101001 format
            returnStr += format(int(i), '08b')
        if (offset + length) < len(returnStr):
            return int(returnStr[offset : (offset+length)])
        else:
            return -1

    def ReceiveMessage(self):
        while True:
            try:
                message = self.Canbus.recv()
                if message:
                    for variable in self.listOfMessagesToRead:
                        if message.arbitration_id == variable.pid: 
                            newValue = self.GetValueByCanMsg(message.data,variable.offset,variable.length)
                            if(newValue != variable.value):
                                variable.value = newValue
                                print(f"Variable {variable.alias} updated to {newValue}")

            except can.CanError as e:
                print(f"Error receiving message: {e}")

    def Begin(self):
        if self.Canbus is None:
            raise RuntimeError("Interface need init first!")
        
        Canbus_SendThread = threading.Thread(target=self.MessageSender)
        Canbus_ReceiveThread = threading.Thread(target=self.ReceiveMessage)

        Canbus_SendThread.start()
        Canbus_ReceiveThread.start()

        Canbus_SendThread.join()
        Canbus_ReceiveThread.join()

        self.Canbus.shutdown()

def main(): 

    # Can bus init
    MbCanB = MBcanbus(Channel.CanB)
    MbCanB.Begin()
   
    # Send value to can bus
    devicePid = 0x1
    msg = [0x3,0x4,0x5,0x3]
    times = -1
    #MbCanB.SendMessage(devicePid, msg, times)
    

    MbCanB.AddCheckList(0x0016, 0, 8, "Battery")
    MbCanB.AddCheckList(0x0000, 3, 1, "Terminal50")
    MbCanB.AddCheckList(0x0000, 5, 1, "Terminal15")

    # Add values checklist
    #devicePid = 0x0200
    #offset = 18
    #length = 14
    #alias = "FrontLeftWheelSpeed"
    #MbCanC.AddCheckList(devicePid, offset, length, alias)

    #MbCanC.AddCheckList(0x0200, 34, 14, "FrontRightWheelSpeed")
    #MbCanC.AddCheckList(0x0208, 34, 14, "RearRightWheelSpeed")
    #MbCanC.AddCheckList(0x0208, 50, 14, "RearLeftWheelSpeed")
  
if __name__ == "__main__": 
    main() 