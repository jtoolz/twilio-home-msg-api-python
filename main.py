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
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.twiml.voice_response import VoiceResponse

# twilio phone # is +12242796236

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

class HelloMonkey(webapp2.RequestHandler):
    def post(self):
        r = VoiceResponse()
        r.say("Hello Pumpkin!!")
        self.response.headers['Content-Type'] = 'text/xml'
        self.response.write(str(r))

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/twiml', HelloMonkey)
	], debug=True)
