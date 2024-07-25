# PythonCanbusHandler

# (CanBusHandler)

With this canbus library, you can handle CAN bus data more easily.

## Installation

```bash
pip install CanBusHandler
```

Usage
Here's a simple example of how to use the CanBusHandler library:

from CanBusHandler import Handler, Channel

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

