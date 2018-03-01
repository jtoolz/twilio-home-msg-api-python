#
# API for retrieving messages
# Code uses Google Cloud Endpoints
#

# [START imports]
import endpoints
import HomeMessage, Sender from models

from protorpc import message_types, messages, remote
# [END imports]

# [START messages]

#
# Define the message that we will send back upon request
# Right now we just want to provide the last message received 
# at the Twilio phone number. Future versions might allow indexing
# back into older messages, or filtering on senders or content
class HomeMessage(messages.Message):
    body = messages.StringField(1, required=True)
    sender = messages.StringField(2, required=True)
    when = messages.IntegerField(3, required=True)

# Example collection for later. Will leave commented out for now:
# class HomeMessageCollection(messages.Message):
#    items = messages.MessageField(HomeMessage, 1, repeated=True)
#

# [END messages]

# [START message API]
@endpoints.api(name='home_message', version='v1')
class HomeMessageApi(remote.Service):
    @endpoints.method(
        # This method takes an empty request body.
        message_types.VoidMessage,
        # This method returns a HomeMessage
        HomeMessage,
        path='getMessage',
        http_method='GET',
        # Require auth tokens to have the following scopes to access this API.
        scopes=[endpoints.EMAIL_SCOPE])
        # OAuth2 audiences allowed in incoming tokens.
        # audiences=['your-oauth-client-id.com'])
    def get_message(self, request):
        user = endpoints.get_current_user()
        # If there's no user defined, the request was unauthenticated, so we
        # raise 401 Unauthorized.
        #if not user:
        #    raise endpoints.UnauthorizedException
        return HomeMessage(body="test message", sender="test sender", when=int("12345678"))

    @endpoints.method(
        message_types.VoidMessage,
        HomeMessage,
        path='postMessage',
        http_method='POST',
        name='home_msg')
    def post_message(self, request):
        return HomeMessage(body="test message", sender="test sender", when=int("12345678"))
# [END message API]

# [START api_server]
api = endpoints.api_server([HomeMessageApi])
# [END api_server]

