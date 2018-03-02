#
# API for retrieving messages
# Code uses Google Cloud Endpoints
#

# [START imports]
import endpoints

from protorpc import remote
from endpoints_proto_datastore.ndb import EndpointsModel

from models import HomeMsgModel
# [END imports]

# [START message API]
@endpoints.api(name='home_message', version='v1', description='API for retrieving messages received via Twilio')
class HomeMessageApi(remote.Service):
    @HomeMsgModel.query_method(path='messages', name='home_msg.get_last')

    def HomeMsgModelList(self, query):
        return query.filter(HomeMsgModel.is_last==True)
        
#    @endpoints.method(
#        message_types.VoidMessage,
#        HomeMessage,
#        path='postMessage',
#        http_method='POST',
#        name='home_msg')
#    def post_message(self, request):
#        return HomeMessage(body="test message", sender="test sender", when=int("12345678"))
# [END message API]

# [START api_server]
api = endpoints.api_server([HomeMessageApi], restricted=False)
# [END api_server]

