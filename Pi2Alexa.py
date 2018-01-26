#!/usr/bin/env python
#
#
# Raspberry Pi to Alexa 
#
# SwitchDoc Labs
#

PI2ALEXAVERSION = "002"

#imports 

import sys
import os
import RPi.GPIO as GPIO
import time
import json

from datetime import datetime
from datetime import timedelta

from pubnub.pubnub import PubNub
from pubnub.pubnub import PNConfiguration
from pubnub.callbacks import SubscribeCallback


# debug setting
DEBUG = True

# PubNub configuration

Pubnub_Publish_Key = "pub-c-xxx"
Pubnub_Subscribe_Key = "sub-c-xxx"

#GPIO LED Pin configuration

LED_PIN=4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(LED_PIN,GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)


#GPIO State

LED_State = "Off"

pnconf = PNConfiguration()
 
pnconf.subscribe_key = Pubnub_Subscribe_Key
pnconf.publish_key = Pubnub_Publish_Key
  

pubnub = PubNub(pnconf)

def publish_callback(result, status):
        if (DEBUG):
		print "status.is_error", status.is_error()
		print "status.original_response", status.original_response
		pass
        # handle publish result, status always present, result if successful
        # status.isError to see if error happened

def publishStatusToPubNub():

        myMessage = {}
        myMessage["Pi2Alexa_CurrentStatus"] = "Active" 
	myMessage["Pi2Alexa_Version"] = '{}'.format(PI2ALEXAVERSION) 
        myMessage["TimeStamp"] = '{}'.format( datetime.now().strftime( "%m/%d/%Y %H:%M:%S"))
        myMessage["Pi2Alexa_LEDState"] = LED_State 
        
        if (DEBUG):
        	print myMessage

        pubnub.publish().channel('Pi2Alexa_Status').message(myMessage).async(publish_callback)



 
class AlexaMyListener(SubscribeCallback):
    def status(self, pubnub, status):
	pass 
    def message(self, pubnub, message):
        global LED_State
	print "message=", message.message
	# set LED commands
	LED_State = message.message["LED"]
        print "LED_State = ", LED_State

	if (LED_State == "Off"):
		GPIO.output(LED_PIN, GPIO.LOW)

	if (LED_State == "On"):
		GPIO.output(LED_PIN, GPIO.HIGH)

 
    def presence(self, pubnub, presence):
        pass

# set up subscribe channel

my_listener = AlexaMyListener()
 
pubnub.add_listener(my_listener)
 
pubnub.subscribe().channels("Pi2Alexa_Data").execute()


while True:

	publishStatusToPubNub()
	time.sleep(60.0)	

