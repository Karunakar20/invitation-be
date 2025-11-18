# from enum import Enum

# class ResponseType(Enum):
#     success = 0
#     err = 1
#     info = 2
#     warn = 3 
    
# class Response:
     
#      def __init__(self, pOk: bool = True, pDinResponseType: ResponseType = ResponseType.success, pMessage = '', pError = '',pResponse = None):
#           self.ok = pOk
#           self.type = pDinResponseType.value      
#           self.msg = pMessage
#           self.error = pError
#           self.response = pResponse

#      def toJson(self):
#           content = {
#                'ok':self.ok,
#                'type':self.type,
#                'message':self.msg.capitalize() if self.msg else self.msg, 
#                'error': self.error.capitalize() if self.error else self.error, 
#                'response':self.response
#                }
#           return content 