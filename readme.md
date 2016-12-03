# What it does
This is a MQTT chat client that will communicate with other MQTT chat clients via an MQTT server.

It is basically a shell around the MQTT python library which provides a text-based interface for sending and recieving messages over MQTT.
The overall flow is:
1. Subscribe to the user-specified channel on the user-specified, in order to receive messages
2. Display messages 
2. Wait for user input, and publish messages to the channel
 This client can publish messages to a channel. to a ch simultaneously subscribe to a channel on a connect to a MQTT server, and communicate with it.

# Notes
- We are using threads so we can get user input while listening for messages
 - Idea from:
  - http://stackoverflow.com/questions/22240533/display-output-while-inside-of-raw-input
  - http://stackoverflow.com/a/22240617
- The Queue library handles locking between threads

# Run the code
1. `git pull`, download, or clone this project (git clone <github URL>)
2. `source venv/bin/activate` to change into the virtual python environment
3. `python main.py` to run the code!

# Mac Visual Studio Code Development Setup

1. Download and install Visual Studio Code for Mac
2. Download (or clone) this project from GitHub to your computer (git clone <github URL>)
3. Open this project in Visual Studio (File, Open..., Navigate to the folder)

