# CanbusHandler
(for python)
With this canbus library, you can handle CAN bus data more easily.

![image](https://github.com/user-attachments/assets/7e15bb34-002b-4576-933a-595057a284bc)
i used 2-Channel Isolated CAN Expansion HAT for Raspberry Pi, Dual Chips Solution
in this project https://www.waveshare.com/2-ch-can-hat.htm
my rasberry pi is 4 model b.


## Installation

```bash
pip install git+https://github.com/jaakka/PythonCanbusHandler.git

```
#Remember start canbus
```
sudo ip link set can0 up type can bitrate 500000
sudo ifconfig can0 up

sudo ip link set can1 up type can bitrate 500000
sudo ifconfig can1 up

```
500000 is 500kbps, you need to find out the right speed for your car.

In my mercedes have two speeds
CanB is for radio, windows, and other amusement devices, speed is 83,3kbps
CanC is for motor and more important devices and speed is 500kbps (+ 5times faster)

Also remember to check that you don't have the end resistors in use, you probably won't need them if you're reading messages from the car

Usage
Here's a simple example of how to use the CanBusHandler library:

from CanbusHandler import Handler, Channel

# Initialize CAN bus on channel B
bus = Handler(Channel.CanB)

# Add variables to monitor
bus.AddCheckList(0x0016, 0, 8, "Battery")

bus.AddCheckList(0x0000, 3, 1, "Terminal50")

bus.AddCheckList(0x0000, 5, 1, "Terminal15")

# Start the CAN bus communication
bus.Begin()

Features
Send and receive CAN messages
Monitor specific variables on the CAN bus

CHECK tutorial.py
