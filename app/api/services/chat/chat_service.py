from datetime import datetime
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.models.chat.chat_group import ChatGroup, ChatMessage
from app.api.utilities.common import Response, ResponseType
from app.api.services.chat.websocket_manager import manager


async def create_chat_group(invitation_id: str, group_name: str, created_by: int, mongodb: AsyncIOMotorDatabase) -> str:
    """Create a new chat group for an invitation"""
    try:
        chat_group = ChatGroup(
            invitation_id=invitation_id,
            group_name=group_name,
            created_by=created_by,
            members=[created_by]  # Creator is automatically a member
        )

        result = await mongodb.chat_groups.insert_one(chat_group.dict(by_alias=True))
        return str(result.inserted_id)

    except Exception as e:
        raise Exception(f"Failed to create chat group: {str(e)}")


async def get_chat_group_by_invitation(invitation_id: str, mongodb: AsyncIOMotorDatabase) -> Optional[ChatGroup]:
    """Get chat group by invitation ID"""
    try:
        group_data = await mongodb.chat_groups.find_one({"invitation_id": invitation_id})
        if group_data:
            return ChatGroup(**group_data)
        return None
    except Exception as e:
        raise Exception(f"Failed to get chat group: {str(e)}")


async def add_member_to_chat_group(chat_group_id: str, user_id: int, mongodb: AsyncIOMotorDatabase) -> bool:
    """Add a member to a chat group"""
    try:
        result = await mongodb.chat_groups.update_one(
            {"_id": chat_group_id},
            {"$addToSet": {"members": user_id}}
        )
        return result.modified_count > 0
    except Exception as e:
        raise Exception(f"Failed to add member to chat group: {str(e)}")


async def send_message(chat_group_id: str, sender_id: int, message: str, mongodb: AsyncIOMotorDatabase, message_type: str = "text") -> str:
    """Send a message to a chat group"""
    try:
        chat_message = ChatMessage(
            chat_group_id=chat_group_id,
            sender_id=sender_id,
            message=message,
            message_type=message_type
        )

        result = await mongodb.chat_messages.insert_one(chat_message.dict(by_alias=True))
        message_id = str(result.inserted_id)

        # Broadcast the message to all connected clients in the chat group
        message_data = {
            "type": "new_message",
            "data": {
                "id": message_id,
                "chat_group_id": chat_group_id,
                "sender_id": sender_id,
                "message": message,
                "message_type": message_type,
                "created_at": chat_message.created_at.isoformat(),
                "is_deleted": False
            }
        }
        await manager.broadcast_to_group(chat_group_id, message_data)

        return message_id

    except Exception as e:
        raise Exception(f"Failed to send message: {str(e)}")


async def get_chat_messages(chat_group_id: str, mongodb: AsyncIOMotorDatabase, limit: int = 50) -> List[ChatMessage]:
    """Get messages from a chat group"""
    try:
        cursor = mongodb.chat_messages.find(
            {"chat_group_id": chat_group_id, "is_deleted": False}
        ).sort("created_at", -1).limit(limit)

        messages = []
        async for message_data in cursor:
            messages.append(ChatMessage(**message_data))

        return messages[::-1]  # Reverse to get chronological order

    except Exception as e:
        raise Exception(f"Failed to get chat messages: {str(e)}")


async def get_user_chat_groups(user_id: int, mongodb: AsyncIOMotorDatabase) -> List[ChatGroup]:
    """Get all chat groups where user is a member"""
    try:
        cursor = mongodb.chat_groups.find({"members": user_id, "is_active": True})

        groups = []
        async for group_data in cursor:
            groups.append(ChatGroup(**group_data))

        return groups

    except Exception as e:
        raise Exception(f"Failed to get user chat groups: {str(e)}")