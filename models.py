import endpoints
from google.appengine.ext import ndb
from endpoints_proto_datastore.ndb import EndpointsModel

DEFAULT_MESSAGELIST_NAME = "default_messagelist"

# We set a parent key to ensure they are all in the same entity
# group. Queries across the entity group will be consistent.
def message_key(messagelist_name = DEFAULT_MESSAGELIST_NAME):
    return ndb.Key('MessageList', messagelist_name)

# [START models]

# Define the message that we will send back upon request
# Right now we just want to provide the last message received 
# at the Twilio phone number. Future versions might allow indexing
# back into older messages, or filtering on senders or content
class HomeMsgModel(EndpointsModel):
    # Borrowed from Endpoints-proto library. Sets exact order of fields
    # in RPC message schema.
    _message_fields_schema = ('sender_name', 'sender_phone', 'content', 'created', 'is_last')

    sender_name = ndb.StringProperty()
    sender_phone = ndb.StringProperty()
    content = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    is_last = ndb.BooleanProperty()

# Whitelist class for filtering incoming messages
class WhitelistModel(ndb.Model):
    sender_name = ndb.StringProperty()
    sender_phone = ndb.StringProperty()

# [END models]