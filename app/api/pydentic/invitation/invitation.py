from pydantic import BaseModel,Field
from typing import Optional,List, Union
from datetime import date, time
from fastapi import UploadFile

class InvitaionProfile(BaseModel):
    id: Optional[str] = None
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
    event_photo: Union[str, UploadFile]

    class Config:
    
        from_attributes = True

class InvitationPydentic(BaseModel):
    id: Optional[str] = None
    # event_type: int
    event_name: str
    venue_location: str
    event_date: date
    event_time: time
    event_photo: Union[str, UploadFile]
    created_by: int
    updated_by : int

    link: Optional[str] = None
    csv_file_path: Optional[str] = None
    qr_code_path: Optional[str] = None

    sub_invitating: List[SubInvitationPydentic] = Field(default_factory=list)

    class Config:
    
        from_attributes = True

class SubInvitationResponse(BaseModel):
    id: int
    event_name: str
    venue_location: str
    event_date: date
    event_start_time: time
    event_end_time: time
    event_photo: str   # ✅ always string

    class Config:
        from_attributes = True


class InvitationResponse(BaseModel):
    id: str
    event_name: str
    venue_location: str
    event_date: date
    event_time: time
    event_photo: str   # ✅ always string

    link: Optional[str]
    csv_file_path: Optional[str]
    qr_code_path: Optional[str]

    sub_invitating: List[SubInvitationResponse]

    class Config:
        from_attributes = True
