from pydantic import BaseModel
from typing import Optional
from datetime import date, time

class SubInvitationPydentic(BaseModel):
    id: Optional[int] = None
    event_type: int
    created_by: int
    event_title: str
    event_date: date
    event_time: time
    venue_name: str
    venue_address: str
    note: Optional[str] = None
    event_photo: str
    link: Optional[str] = None


class InvitationPydentic(BaseModel):
    id: Optional[int] = None
    event_type: int
    created_by: int
    event_title: str
    event_date: date
    event_time: time
    venue_name: str
    venue_address: str
    note: Optional[str] = None
    event_photo: str
    link: Optional[str] = None

    sub_invitating: Optional[SubInvitationPydentic] = None

    name_1: Optional[str] = None
    name_2: Optional[str] = None
    date_1: Optional[date] = None
    date_2: Optional[date] = None
