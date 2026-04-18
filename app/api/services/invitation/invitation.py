from app.api.models.invitation.invitation import Invitation, SubInvitation, InvitationGuests
from app.api.pydentic.invitation.invitation import InvitationPydentic
from app.api.utilities.common import Response, ResponseType


async def _create_or_update_sub_event(db, invi_obj, data: InvitationPydentic):
      for sub_event in data.sub_invitating:
            obj = await db.get(SubInvitation, sub_event.id) if sub_event.id else SubInvitation()

            obj.invitation = invi_obj.id
            obj.event_name = sub_event.event_name
            obj.venue_location = sub_event.venue_location
            obj.event_date = sub_event.event_date
            obj.event_start_time = sub_event.event_start_time
            obj.event_end_time = sub_event.event_end_time
            obj.event_photo = sub_event.event_photo

            if not data.id:
                  db.add(obj)


async def create_or_update_invitation(db, data: InvitationPydentic, err_msg: str):
      try:
            invi_obj = await db.get(Invitation, data.id) if data.id else Invitation()

            invi_obj.event_name = data.event_name
            invi_obj.venue_location = data.venue_location
            invi_obj.event_date = data.event_date
            invi_obj.event_time = data.event_time
            invi_obj.event_photo = data.event_photo
            invi_obj.created_by = data.created_by
            invi_obj.updated_by = data.updated_by
            invi_obj.link = data.link
            invi_obj.qr_code_path = data.qr_code_path
            invi_obj.csv_file_path = data.csv_file_path

            if not data.id:
                  db.add(invi_obj)

            await _create_or_update_sub_event(db, invi_obj, data)

            await db.commit()
            await db.refresh(invi_obj)

            msg = "Updating existing invitation" if data.id else "Creating new invitation"
            return Response(True, ResponseType.success, msg, None, {"response": invi_obj.id})

      except Exception as e:
            await db.rollback()
            return Response(False, ResponseType.err, err_msg, str(e))