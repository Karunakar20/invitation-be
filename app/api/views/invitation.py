from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from api.services.invitation.invitation import InvitationService
from api.pydentic.invitation.invitation import InvitationPydentic

from core.db.db_config import db_connection

router = APIRouter(prefix="/service",tags=["service"])


@router.post("/invitation/")
def manage_invitation(cmd: str, data: InvitationPydentic, db: Session = Depends(db_connection)):
    mRet = InvitationService(cmd, data, db).manage()
    return mRet.toJson()

@router.get("/invitation/")
def get_invitation(cmd: str, db: Session = Depends(db_connection)):
    mRet = InvitationService(cmd, None, db).manage()
    return mRet.toJson()