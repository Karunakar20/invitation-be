from models.invitation.invitation import Invitation,SubInvitation,InvitationProfile,InvitationGuests,SubInvitationGuests
from pydentic.invitation.invitation import InvitationPydentic
from api.utilities.common import Response,ResponseType
class InvitationService:
      def __init__(self,cmd,data:InvitationPydentic):
            self.cmd = cmd
            self.data = data

      def __createOrUpdate(self):
            try:
                  None
            except Exception as e:
                  return Response(False,ResponseType.err,self.err_msg,str(e))

      def manage(self):
            match self.cmd:
                  case 'create':
                        self.sucess_msg = 'Invitation created Suceessfully'
                        self.err_msg = 'Unable to send invitation'
                        return self.__createOrUpdate()
                  
                  case 'edit':
                        self.sucess_msg = 'Invitation edited Suceessfully'
                        self.err_msg = 'Unable to edit invitation'
                        return self.__createOrUpdate()


      




      