from fastapi import APIRouter

from api.services.invitation.invitation import InvitationService
from api.pydentic.invitation.invitation import InvitationPydentic

router = APIRouter(prefix="/service",tags=["service"])


@router.post("/invitation/")
def manage_invitation(cmd: str ,data:InvitationPydentic):
    mRet = InvitationService(cmd,data).manage()
    return mRet.toJson()

@router.get("/invitation/")
def get_invitation(cmd: str):
    mRet = InvitationService(cmd).manage()
    return mRet.toJson()