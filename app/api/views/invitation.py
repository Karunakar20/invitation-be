from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from app.api.services.invitation.invitation import create_or_update_invitation
from app.api.pydentic.invitation.invitation import InvitationPydentic

from app.core.db.db_config import db_connection

router = APIRouter(prefix="/service",tags=["Invitation"])


@router.post("/invitation/")
def manage_invitation(data: InvitationPydentic, db: Session = Depends(db_connection)):
    mRet = create_or_update_invitation(data, db)
    return mRet

@router.get("/invitation/")
def get_invitation(db: Session = Depends(db_connection)):
    mRet = create_or_update_invitation(None, db)
    return mRet