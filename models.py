import endpoints
from google.appengine.ext import ndb
from protorpc import remote

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
class HomeMsgModel(ndb.Model):
    sender_name = ndb.StringProperty(indexed=False)
    sender_phone = ndb.StringProperty()
    content = ndb.StringProperty(indexed=False)
    created = ndb.DateTimeProperty(auto_now_add=True)
    is_last = ndb.BooleanProperty()

# Whitelist class for filtering incoming messages
class WhitelistModel(ndb.Model):
    sender_name = ndb.StringProperty()
    sender_phone = ndb.StringProperty()

# [END models]