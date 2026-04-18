from app.api.models.invitation.invitation import Invitation, SubInvitation, InvitationGuests
from app.api.pydentic.invitation.invitation import InvitationPydentic
from app.api.utilities.common import Response, ResponseType
from sqlalchemy import select


async def _create_or_update_sub_event(db, invi_obj: Invitation, data: InvitationPydentic):
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


async def create_or_update_invitation(data: InvitationPydentic, db):
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
                  # allocate primary key before creating sub-events
                  await db.flush()

            await _create_or_update_sub_event(db, invi_obj, data)

            await db.commit()
            await db.refresh(invi_obj)

            msg = "Updating existing invitation" if data.id else "Creating new invitation"
            return Response(True, ResponseType.success, msg, None, {"response": invi_obj.id})

      except Exception as e:
            await db.rollback()
            return Response(False, ResponseType.err, "Unable to save invitation", str(e))


async def get_invitations(db):
      try:
            result = await db.execute(select(Invitation))
            invitations = result.scalars().all()
            data = [
                  {
                        "id": i.id,
                        "event_name": i.event_name,
                        "event_date": i.event_date,
                        "event_time": i.event_time,
                        "venue_location": i.venue_location,
                        "link": i.link,
                  }
                  for i in invitations
            ]
            return Response(True, ResponseType.success, None, None, data)
      except Exception as e:
            return Response(False, ResponseType.err, "Unable to fetch invitations", str(e))


async def get_invitation_by_id(invitation_id: int, db):
      try:
            invitation = await db.get(Invitation, invitation_id)
            if not invitation:
                  return Response(False, ResponseType.err, "Invitation not found", None, None)

            data = {
                  "id": invitation.id,
                  "event_name": invitation.event_name,
                  "event_date": invitation.event_date,
                  "event_time": invitation.event_time,
                  "venue_location": invitation.venue_location,
                  "event_photo": invitation.event_photo,
                  "created_by": invitation.created_by,
                  "updated_by": invitation.updated_by,
                  "link": invitation.link,
                  "csv_file_path": invitation.csv_file_path,
                  "qr_code_path": invitation.qr_code_path,
            }
            return Response(True, ResponseType.success, None, None, data)
      except Exception as e:
            return Response(False, ResponseType.err, "Unable to fetch invitation", str(e))