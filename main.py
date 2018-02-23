# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import os
import logging
import json

from flask import Flask, request
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.twiml.voice_response import VoiceResponse

from google.appengine.ext import ndb

# Config settings
TWILIO_PHONE_NUM = os.environ['TWILIO_PHONE_NUM']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_ACCT_SID = os.environ['TWILIO_ACCT_SID']
WHITELIST_FILE = os.environ['WHITELIST_FILE']
DEFAULT_MESSAGELIST_NAME = "default_messagelist"
# End config

whitelist = {"+15555551212":"Test1", "+15555551212":"Test2"}

app = Flask(__name__)

def load_whitelist():
	logging.info("loading whitelist() from " + WHITELIST_FILE)
	f = open(WHITELIST_FILE)
	logging.info("f is" + str(f))
	return json.load(f)

# We set a parent key to ensure they are all in the same entity
# group. Queries across the entity group will be consistent.
def message_key(messagelist_name = DEFAULT_MESSAGELIST_NAME):
	return ndb.Key('MessageList', messagelist_name)

class Sender(ndb.Model):
	name = ndb.StringProperty(indexed=False)
	phone_num = ndb.StringProperty()

class HomeMessage(ndb.Model):
	sender = ndb.StructuredProperty(Sender)
	content = ndb.StringProperty(indexed=False)
	timestamp = ndb.DateTimeProperty(auto_now_add=True)

@app.route('/call/receive', methods=['POST'])
def receive_voice():
    r = VoiceResponse()
    r.say("Hello Pumpkin!!")    
    return str(r), 200, {'Content-Type': 'application/xml'}

#	
# Receive an SMS message and put it in datastore
# Only accept from known numbers in address book 
@app.route('/sms/receive', methods=['POST'])
def receive_sms():
    sender = str(request.values.get('From'))
    body = str(request.values.get('Body'))
    logging.info("received msg " + str(body) + " from " + str(sender))
#    if (any(whitelist.values()) is False):
#    	load_whitelist()

    logging.info("whitelist is " + str(whitelist))
    
    if (sender in whitelist.keys()):
    	logging.info("found key " + sender + " in whitelist")
        homemsg = HomeMessage(parent=message_key())
        homemsg.sender = Sender(name=whitelist[sender], phone_num=sender)
        homemsg.content = body
        logging.info("set body " + str(body))
        homemsg.put()

    message = 'Hello, {}, you said: {}'.format(sender, body)

    response = MessagingResponse()
    response.message(message)
    return str(response), 200, {'Content-Type': 'application/xml'}
    

if __name__ == '__main__':
    
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
