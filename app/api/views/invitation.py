from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from app.api.services.invitation.invitation import create_or_update_invitation
from app.api.pydentic.invitation.invitation import InvitationPydentic

from app.core.db.db_config import db_connection

router = APIRouter(prefix="/service",tags=["Invitation"])


@router.post("/invitation/")
def manage_invitation(cmd: str, data: InvitationPydentic, db: Session = Depends(db_connection)):
    mRet = create_or_update_invitation(cmd, data, db)
    return mRet.toJson()

@router.get("/invitation/")
def get_invitation(cmd: str, db: Session = Depends(db_connection)):
    mRet = create_or_update_invitation(cmd, None, db)
    return mRet.toJson()