from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, model_serializer
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {"type": "string"}


class ChatGroup(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    invitation_id: str  # UUID of the invitation
    group_name: str
    created_by: int  # User ID who created the invitation
    created_at: datetime = Field(default_factory=datetime.utcnow)
    members: List[int] = Field(default_factory=list)  # List of user IDs
    is_active: bool = True

    model_config = {
        "validate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

    @model_serializer(mode='plain')
    def serialize_model(self):
        data = {}
        for key, value in self.__dict__.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)
            else:
                data[key] = value
        # Handle alias for id field
        if '_id' in data:
            data['id'] = data.pop('_id')
        return data


class ChatMessage(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    chat_group_id: str  # ObjectId as string
    sender_id: int
    message: str
    message_type: str = "text"  # text, image, file, etc.
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_deleted: bool = False

    model_config = {
        "validate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

    @model_serializer(mode='plain')
    def serialize_model(self):
        data = {}
        for key, value in self.__dict__.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)
            else:
                data[key] = value
        # Handle alias for id field
        if '_id' in data:
            data['id'] = data.pop('_id')
        return data