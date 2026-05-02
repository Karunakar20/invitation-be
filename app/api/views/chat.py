from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

from app.api.models.chat.chat_group import ChatGroup, ChatMessage
from app.api.services.chat.chat_service import (
    get_chat_group_by_invitation,
    send_message,
    get_chat_messages,
    get_user_chat_groups
)
from app.api.services.chat.websocket_manager import manager
from app.core.db.mongodb_config import get_mongodb

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.get("/group/{invitation_id}")
async def get_chat_group(invitation_id: str, mongodb: AsyncIOMotorDatabase = Depends(get_mongodb)):
    """Get chat group for an invitation"""
    try:
        group = await get_chat_group_by_invitation(invitation_id, mongodb)
        if not group:
            raise HTTPException(status_code=404, detail="Chat group not found")
        return {"success": True, "data": group.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/group/{chat_group_id}/message")
async def send_chat_message(
    chat_group_id: str,
    sender_id: int,
    message: str,
    message_type: str = "text",
    mongodb: AsyncIOMotorDatabase = Depends(get_mongodb)
):
    """Send a message to a chat group"""
    try:
        message_id = await send_message(chat_group_id, sender_id, message, mongodb, message_type)
        return {"success": True, "message_id": message_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/group/{chat_group_id}/messages")
async def get_group_messages(
    chat_group_id: str,
    limit: int = 50,
    mongodb: AsyncIOMotorDatabase = Depends(get_mongodb)
):
    """Get messages from a chat group"""
    try:
        messages = await get_chat_messages(chat_group_id, mongodb, limit)
        return {"success": True, "data": [msg.dict() for msg in messages]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{user_id}/groups")
async def get_user_groups(user_id: int, mongodb: AsyncIOMotorDatabase = Depends(get_mongodb)):
    """Get all chat groups for a user"""
    try:
        groups = await get_user_chat_groups(user_id, mongodb)
        return {"success": True, "data": [group.dict() for group in groups]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.websocket("/ws/{chat_group_id}")
async def websocket_endpoint(websocket: WebSocket, chat_group_id: str):
    """WebSocket endpoint for real-time chat in a chat group"""
    await manager.connect(websocket, chat_group_id)
    try:
        while True:
            # Wait for messages from the client
            data = await websocket.receive_json()

            # Handle different message types
            if data.get("type") == "join":
                # Client joined the chat group
                await manager.send_personal_message({
                    "type": "joined",
                    "data": {"chat_group_id": chat_group_id}
                }, websocket)

            elif data.get("type") == "message":
                # Client sent a message - this will be handled by the HTTP endpoint
                # But we can acknowledge receipt
                await manager.send_personal_message({
                    "type": "message_received",
                    "data": {"message": "Message sent via HTTP endpoint"}
                }, websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket, chat_group_id)