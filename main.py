"""Main python file for chat client"""
# This is meant to run in Python 3, not Python 2
# DISCLAIMER: Some code based on ideas hbmqtt documentation,
# and some from code borrowed from hbmqtt example code:
# https://hbmqtt.readthedocs.io/en/latest/references/mqttclient.html

import asyncio
import hbmqtt
from hbmqtt import client as hbmqttclient
from threading import Thread
import queue
from time import sleep
from random import random

CLIENT_ID_LENGTH = 5
# Get random CLIENT_ID_LENGTH digit string of numbers
CLIENT_ID = (("%." + str(CLIENT_ID_LENGTH) + "f") % random())[2:]

# MQTT_BROKER_URI = "mqtt://localhost:1883"
MQTT_BROKER_URI = "mqtt://broker.hivemq.com:1883"
CHANNEL_ID = "unofouramigos/chat1"

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

inputThread = Thread(target=getNextInputLine)
inputThread.start()

print("Hello! You are client " + CLIENT_ID)
print()

@asyncio.coroutine
def beginMQTTClient():
    client = hbmqttclient.MQTTClient()
    yield from client.connect(MQTT_BROKER_URI)
    yield from client.subscribe([(CHANNEL_ID, hbmqtt.mqtt.constants.QOS_0)])
    while True:
        weGotMail = False
        try:
            msg = yield from client.deliver_message(timeout=.1)
            weGotMail = True
        except asyncio.TimeoutError:
            pass

        # Handle local user trying to send a message
        try:
            inputLine = inputQueue.get_nowait()
            # print("Oh hey! A message from the user:")
            # print(inputLine)
            response = CLIENT_ID + " " + inputLine
            yield from client.publish(CHANNEL_ID, bytearray(response, "utf-8"))

        except queue.Empty:
            pass # No new user input

        if weGotMail:
            # Help from internal python docs on bytearray
            rawStrMsg = msg.data.decode("utf-8")
            clientId = rawStrMsg[0:CLIENT_ID_LENGTH]
            textMessage = rawStrMsg[CLIENT_ID_LENGTH+1:]

            # Ignore messages sent by us
            if clientId == CLIENT_ID:
                continue

            print("Client " + clientId + ": " + textMessage)
            # response = CLIENT_ID + "Thanks!"
            # yield from client.publish("blue", bytearray(response, "utf-8"))
            # "blue", "Why thank you", client " + clientId + " for sending us " + textMessage"

asyncio.get_event_loop().run_until_complete(beginMQTTClient())


