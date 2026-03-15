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
    event_name: str
    venue_location: str
    event_date: date
    event_start_time: time
    event_end_time: time
    event_photo: str

class InvitationPydentic(BaseModel):
    id: Optional[int] = None
    # event_type: int
    event_name: str
    venue_location: str
    event_date: date
    event_time: time
    event_photo: str
    created_by: int
    updated_by : int

    event_photo: str
    link: Optional[str] = None
    csv_file_path: Optional[str] = None
    qr_code_path: Optional[str] = None

    sub_invitating: List[SubInvitationPydentic] = Field(default_factory=list)
