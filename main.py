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

from flask import Flask, request
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.twiml.voice_response import VoiceResponse

# Config settings
TWILIO_PHONE_NUM = os.environ['TWILIO_PHONE_NUM']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_ACCT_SID = os.environ['TWILIO_ACCT_SID']
# End config

app = Flask(__name__)

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
    sender = request.values.get('From')
    body = request.values.get('Body')

    message = 'Hello, {}, you said: {}'.format(sender, body)

    response = MessagingResponse()
    response.message(message)
    return str(response), 200, {'Content-Type': 'application/xml'}
    

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
