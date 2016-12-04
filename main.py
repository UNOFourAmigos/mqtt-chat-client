"""Main python file for chat client"""
# This is meant to run in Python 3, not Python 2
# DISCLAIMER: Some code borrowed from hbmqtt library example documentation:
# https://hbmqtt.readthedocs.io/en/latest/references/mqttclient.html

import asyncio
import hbmqtt
from hbmqtt import client as hbmqttclient
from threading import Thread
import queue
from time import sleep
from random import random

# Get random 10 digit string of numbers
CLIENT_ID = ("%.10f" % random())[2:]

MQTT_BROKER_URI = "mqtt://localhost:1883"
inputQueue = queue.Queue()

# - We are using threads so we can get user input while listening for messages
#  - Idea from:
#   - http://stackoverflow.com/questions/22240533/display-output-while-inside-of-raw-input
#   - http://stackoverflow.com/a/22240617
def getNextInputLine():
    # http://stackoverflow.com/questions/11786530/can-python-threads-access-variables-in-the-namespace
    # http://stackoverflow.com/a/11786875
    # http://stackoverflow.com/a/11786688
    # http://stackoverflow.com/a/11786684
    # http://stackoverflow.com/questions/370357/python-variable-scope-error
    # http://stackoverflow.com/a/370363
    # http://stackoverflow.com/a/370380
    # http://stackoverflow.com/questions/4693120/use-of-global-keyword-in-python
    # http://stackoverflow.com/a/4693385
    # http://stackoverflow.com/a/4693170
    # http://stackoverflow.com/questions/4744426/python-threading-with-global-variables
    # http://stackoverflow.com/a/4745007
    global inputQueue
    while True:
        inputLine = input()
        inputQueue.put(inputLine)

# inputThread = Thread(target=getNextInputLine)
# inputThread.start()



@asyncio.coroutine
def beginMQTTClient():
    client = hbmqttclient.MQTTClient()
    yield from client.connect(MQTT_BROKER_URI)
    yield from client.subscribe([("blue", hbmqtt.mqtt.constants.QOS_0)])
    while True:
        weGotMail = False
        try:
            msg = yield from client.deliver_message(timeout=.1)
            weGotMail = True
        except asyncio.TimeoutError:
            print("No message received")

        if weGotMail:
            # Help from internal python docs on bytearray
            rawStrMsg = msg.data.decode("utf-8")
            clientId = rawStrMsg[0:10]
            textMessage = rawStrMsg[10:]

            # Ignore messages sent by us
            if clientId == CLIENT_ID:
                continue

            print("Message received from client " + clientId + ": " + textMessage)
            response = CLIENT_ID + "Thanks!"
            yield from client.publish("blue", bytearray(response, "utf-8"))
            # "blue", "Why thank you", client " + clientId + " for sending us " + textMessage"

asyncio.get_event_loop().run_until_complete(beginMQTTClient())

# while True:
    # x = client.deliver_message()
    # print("Message received!")
    # print x

# for i in range(100):
#     # Try to get user input
#     try:
#         inputLine = inputQueue.get_nowait()
#         print("Oh hey! A message from the user:")
#         print(inputLine)
#     except queue.Empty:
#         pass # No new user input
#     print(i)
#     sleep(.2)

