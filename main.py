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
import pdb

# from google.appengine.ext import ndb

from flask import Flask, request
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.twiml.voice_response import VoiceResponse

from models import HomeMsgModel, WhitelistModel, message_key


# Config settings
TWILIO_PHONE_NUM = os.environ['TWILIO_PHONE_NUM']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_ACCT_SID = os.environ['TWILIO_ACCT_SID']
# End config

app = Flask(__name__)

def get_last_msg():
    q = LastMsgModel.all(keys_only=True)
    logging.info("created query")
    return q.get()


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
    # pdb.set_trace()
    # Get SMS data from Twilio
    sender_phone = str(request.values.get('From'))
    body = str(request.values.get('Body'))
    logging.info("received msg " + body + " from " + sender_phone)

    # Check sender phone # against whitelist. We only want messages
    # from sources on the list:
    query = WhitelistModel.query().filter(WhitelistModel.sender_phone==sender_phone)
    whitelist_result = query.get()
    if (whitelist_result is not None):
        # Check to see if we've received a message already. If so,
        # set it's is_last property to False
        query = HomeMsgModel.query().filter(HomeMsgModel.is_last==True)
        msg_result = query.get()
        if (msg_result is not None):
            # Update is_last
            msg_result.is_last=False
            msg_result.put()
        
        # Add new message to the Datastore and mark it as last:
        home_msg = HomeMsgModel(
            parent=message_key(),
            sender_name = whitelist_result.sender_name,
            sender_phone = sender_phone,
            content = body,
            is_last=True)
        msg_key = home_msg.put()        

    message = 'Hello, {}, you said: {}'.format(sender_phone, body)

    response = MessagingResponse()
    response.message(message)
    return str(response), 200, {'Content-Type': 'application/xml'}
    

if __name__ == '__main__':
    
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
