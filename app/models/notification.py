from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class NotificationType(str, enum.Enum):
    EMAIL = "email"
    SMS = "sms"
    IN_APP = "in_app"

class NotificationStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    type = Column(Enum(NotificationType))
    title = Column(String(255))
    content = Column(Text)
    status = Column(Enum(NotificationStatus), default=NotificationStatus.PENDING)
    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, type={self.type})>"
