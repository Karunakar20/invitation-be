from fastapi import APIRouter,Depends,UploadFile, File, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.api.services.invitation.invitation import (
    create_or_update_invitation,
    get_invitations,
    get_invitation_by_id,
)
from app.api.pydentic.invitation.invitation import InvitationPydentic

from app.core.db.db_config import db_connection

router = APIRouter(prefix="/service",tags=["Invitation"])


# {
#   "event_name": "Wedding",
#   "venue_location": "Hyderabad",
#   "event_date": "2026-05-01",
#   "event_time": "18:00:00",
#   "created_by": 1,
#   "updated_by": 1,
#   "sub_invitating": [
#     {
#       "event_type": 1,
#       "created_by": 1,
#       "event_name": "Haldi",
#       "venue_location": "Home",
#       "event_date": "2026-04-30",
#       "event_start_time": "10:00:00",
#       "event_end_time": "12:00:00"
#     }
#   ]
# }

@router.post("/invitation/")
async def manage_invitation(
    data: str = Form(...),  # JSON string
    event_photo: UploadFile = File(...),
    sub_event_photos: list[UploadFile] = File([]),
    db: AsyncSession = Depends(db_connection)
):
    parsed = json.loads(data)

    # attach main image
    parsed["event_photo"] = event_photo

    # attach sub-event images (order-based mapping)
    for i, sub in enumerate(parsed.get("sub_invitating", [])):
        if i < len(sub_event_photos):
            sub["event_photo"] = sub_event_photos[i]

    mRet = await create_or_update_invitation(
        InvitationPydentic(**parsed),
        db
    )
    return mRet.toJson()


@router.get("/invitation/")
async def get_invitation(db: AsyncSession = Depends(db_connection)):
    mRet = await get_invitations(db)
    return mRet.toJson()


@router.get("/invitation/{invitation_id}")
async def get_invitation_id(invitation_id: int, db: AsyncSession = Depends(db_connection)):
    mRet = await get_invitation_by_id(invitation_id, db)
    return mRet.toJson()

