from pydantic import BaseModel, EmailStr, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.models.notification import NotificationType, NotificationStatus

class NotificationBase(BaseModel):
    user_id: int
    type: NotificationType
    title: str
    content: str

class NotificationCreate(NotificationBase):
    # Additional fields for different notification types
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    @validator('email')
    def validate_email(cls, v, values):
        if values.get('type') == NotificationType.EMAIL and not v:
            raise ValueError('Email is required for email notifications')
        return v

    @validator('phone_number')
    def validate_phone(cls, v, values):
        if values.get('type') == NotificationType.SMS and not v:
            raise ValueError('Phone number is required for SMS notifications')
        return v

class NotificationResponse(NotificationBase):
    id: int
    status: NotificationStatus
    retry_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class NotificationList(BaseModel):
    notifications: List[NotificationResponse]
    total: int
