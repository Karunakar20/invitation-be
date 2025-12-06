from pydantic import BaseModel,Field
from typing import Optional,List
from datetime import date, time

class InvitaionProfile(BaseModel):
    id: Optional[int] = None
    name_1: Optional[str] = None
    name_2: Optional[str] = None
    date_1: Optional[date] = None
    date_2: Optional[date] = None


class SubInvitationPydentic(BaseModel):
    id: Optional[int] = None
    event_type: int
    created_by: int
    event_title: str
    event_start_date: date
    event_start_time: time
    event_end_date: date
    event_end_time: time
    venue_name: str
    venue_address: str
    note: Optional[str] = None
    event_photo: str
    link: Optional[str] = None


class InvitationPydentic(BaseModel):
    id: Optional[int] = None
    event_type: int
    created_by: int
    updated_by : int

    sub_invitating: List[SubInvitationPydentic] = Field(default_factory=list)
    invitation_profile : Optional[InvitaionProfile]= None
