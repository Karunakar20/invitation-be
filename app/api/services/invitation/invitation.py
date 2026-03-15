
from api.models.invitation.invitation import Invitation,SubInvitation,InvitationGuests
from api.pydentic.invitation.invitation import InvitationPydentic
from api.utilities.common import Response,ResponseType

class InvitationService:
      def __init__(self,cmd,data:InvitationPydentic,db):
            self.cmd = cmd
            self.data = data
            self.db = db

      def __createOrUpdateSubEvent(self):
            
            for sub_even in self.data.sub_invitating:

                  obj = self.db.get(SubInvitation, sub_even.id) if sub_even.id else SubInvitation()

                  obj.invitation = self.invi_obj.id
                  obj.event_name = sub_even.event_name
                  obj.venue_location = sub_even.venue_location
                  obj.event_date = sub_even.event_date
                  obj.event_start_time = sub_even.event_start_time
                  obj.event_end_time = sub_even.event_end_time
                  obj.event_photo = sub_even.event_photo

                  if not self.data.id:
                        self.db.add(obj)

      # def __createOrUpdateInvitationProfile(self):

      #       obj = self.db.get(InvitationProfile, self.data.invitation_profile.id) if self.data.invitation_profile.id.id else SubInvitation()

      #       obj.invitation = self.invi_obj.id
      #       obj.name_1 = self.data.invitation_profile.name_1
      #       obj.name_2 = self.data.invitation_profile.name_2

      #       if not self.data.id:
      #             self.db.add(obj)

      def __createOrUpdate(self):
        
            try:
                  # find existing or create new
                  self.invi_obj = self.db.get(Invitation, self.data.id) if self.data.id else Invitation()

                  # assign fields dy
                  self.invi_obj.event_name = self.data.event_name
                  self.invi_obj.venue_location = self.data.venue_location
                  self.invi_obj.event_date = self.data.event_date
                  self.invi_obj.event_time = self.data.event_time
                  self.invi_obj.event_photo = self.data.event_photo
                  self.invi_obj.created_by = self.data.created_by
                  self.invi_obj.updated_by = self.data.updated_by

                  self.invi_obj.link = self.data.link
                  self.invi_obj.qr_code_path = self.data.qr_code_path
                  self.invi_obj.csv_file_path = self.data.csv_file_path


                  # new object? => add it
                  if not self.data.id:
                        self.db.add(self.invi_obj)

                  self.__createOrUpdateSubEvent()

                  # self.__createOrUpdateInvitationProfile()

                  self.db.commit()
                  self.db.refresh(self.invi_obj)

                  return Response(True, ResponseType.success, "Saved successfully",None,{"response":self.invi_obj.id})

            except Exception as e:
                  self.db.rollback()
                  return Response(False, ResponseType.err, self.err_msg, str(e))
            
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


      




      