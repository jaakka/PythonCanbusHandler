from CanbusHandler import Handler, Channel

# i used 2-Channel Isolated CAN Expansion HAT for Raspberry Pi, Dual Chips Solution
# in this project https://www.waveshare.com/2-ch-can-hat.htm

# Initialize CAN bus on channel B
busB = Handler(Channel.CanB)

# Initialize CAN bus on channel A
busA = Handler(Channel.CanA)


# Add variables to monitor
devicePid = 0x0016
offset = 0
length = 8
alias = "Battery"
busB.AddCheckList(devicePid, offset, length, alias)

#or just
busB.AddCheckList(0x0000, 3, 1, "Terminal50")

busB.AddCheckList(0x0000, 5, 1, "Terminal15")

# Start the CAN bus communication
busB.Begin()

#read value from checklist, if value not exist returns 0
battery_voltage = busB.GetValue("Battery") 

# Send value to can bus
devicePid = 0x1
msg = [0x3,0x4,0x5,0x3]
times = -1 #send every second and never stop
busB.SendMessage(devicePid, msg, times) 

devicePid = 0x1
msg = [0x3,0x4,0x5,0x3]
times = 13 #send every second 13 times
busA.SendMessage(devicePid, msg, times)