from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.services.invitation.invitation import (
    create_or_update_invitation,
    get_invitations,
    get_invitation_by_id,
)
from app.api.pydentic.invitation.invitation import InvitationPydentic

from app.core.db.db_config import db_connection

router = APIRouter(prefix="/service",tags=["Invitation"])


@router.post("/invitation/")
async def manage_invitation(data: InvitationPydentic, db: AsyncSession = Depends(db_connection)):
    mRet = await create_or_update_invitation(data, db)
    return mRet.toJson()

@router.get("/invitation/")
async def get_invitation(db: AsyncSession = Depends(db_connection)):
    mRet = await get_invitations(db)
    return mRet.toJson()


@router.get("/invitation/{invitation_id}")
async def get_invitation_id(invitation_id: int, db: AsyncSession = Depends(db_connection)):
    mRet = await get_invitation_by_id(invitation_id, db)
    return mRet.toJson()

