from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.models.users.users import Users
from app.core.security.token_auth import create_access_token
from app.core.security.password_validation import hash_password, verify_password
from app.api.utilities.common import Response, ResponseType

async def register_user(db: AsyncSession, data):
    try:
        result = await db.execute(select(Users).where(Users.email == data.email))
        existing = result.scalar_one_or_none()

        if existing:
            raise Exception("User already exists")

        user = Users(
            user_name=data.user_name,
            email=data.email,
            password=hash_password(data.password),
            auth_provider="local",
            is_verified=True
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        token = create_access_token({"user_id": user.id})

        return {
            "user_id": user.id,
            "access_token": token
        }
    except Exception as e:
        return Response(False,ResponseType.err,str(e))

async def login_user(db: AsyncSession, data):
    try:
        result = await db.execute(select(Users).where(Users.email == data.email))
        user = result.scalar_one_or_none()

        if not user:
            raise Exception("User not found")

        if user.auth_provider != "local":
            raise Exception("Use Google login")

        if not verify_password(data.password, user.password):
            raise Exception("Invalid credentials")

        token = create_access_token({"user_id": user.id})

        return {
            "user_id": user.id,
            "access_token": token
        }
    except Exception as e:
        return Response(False,ResponseType.err,str(e))

async def google_auth(db: AsyncSession, data):
    try:
        result = await db.execute(select(Users).where(Users.email == data.email))
        user = result.scalar_one_or_none()

        if not user:
            user = Users(
                email=data.email,
                user_name=data.user_name,
                oauth_id=data.oauth_id,
                profile_pic=data.profile_pic,
                auth_provider="google",
                is_verified=True
            )

            db.add(user)
            await db.commit()
            await db.refresh(user)

        else:
            user.oauth_id = data.oauth_id
            user.profile_pic = data.profile_pic
            await db.commit()

        token = create_access_token({"user_id": user.id})

        return {
            "user_id": user.id,
            "access_token": token
        }
    except Exception as e:
        return Response(False,ResponseType.err,str(e))