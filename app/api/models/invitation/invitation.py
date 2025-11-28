from sqlalchemy import Column, String, Integer, ForeignKey,Date,Time,Boolean
from core.db.database import Base

from api.utilities.common import Response,ResponseType

class Invitation(Base):
      id = Column(Integer, primary_key=True, index=True)
      event_type = Column(Integer, ForeignKey("tb_category.id", ondelete="CASCADE"))
      created_by = Column(Integer, ForeignKey("tb_users.id", ondelete="CASCADE"))

      event_title = Column(String(250))
      event_date = Column(Date)
      event_time = Column(Time)

      venue_name = Column(String(250))
      venue_address = Column(String(250))

      note = Column(String(250),nullable=True)
      event_photo = Column(String)

      link = Column(String,nullable=True)

      __tablename__ = "tb_invitation"

class SubInvitation(Base):
      id = Column(Integer, primary_key=True, index=True)
      event_type = Column(Integer, ForeignKey("tb_sub_category.id", ondelete="CASCADE"))
      created_by = Column(Integer, ForeignKey("tb_users.id", ondelete="CASCADE"))
      event_title = Column(String(250))
      event_date = Column(Date)
      event_time = Column(Time)
      venue_name = Column(String(250))
      venue_address = Column(String(250))
      note = Column(String(500),nullable=True)
      event_photo = Column(String,nullable=True)
      links = Column(String,nullable=True)

      __tablename__ = "tb_sub_invitation"

class InvitationProfile(Base):
      id = Column(Integer, primary_key=True, index=True)
      invitation = Column(Integer, ForeignKey("tb_invitation.id", ondelete="CASCADE"))
      name_1 = Column(String(250),nullable=True)
      name_2 = Column(String(250),nullable=True)
      date_1 = Column(Date, nullable=True)
      date_2 = Column(Date, nullable=True)
      is_template_need = Column(Boolean,default=False)

      __tablename__ = "tb_invitation_profile"

class InvitationGuests(Base):
      id = Column(Integer, primary_key=True, index=True)
      invitation = Column(Integer, ForeignKey("tb_invitation.id", ondelete="CASCADE"))
      guest = Column(Integer, ForeignKey("tb_users.id", ondelete="CASCADE"))

      __tablename__ = "tb_invitation_guests"


class SubInvitationGuests(Base):
      id = Column(Integer, primary_key=True, index=True)

      sub_invitation = Column(Integer, ForeignKey("tb_sub_invitation.id", ondelete="CASCADE"))
      guest = Column(Integer, ForeignKey("tb_users.id", ondelete="CASCADE"))

      __tablename__ = "tb_sub_invitation_guests"




