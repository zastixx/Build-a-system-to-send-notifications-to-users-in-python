from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.base import SessionLocal
from app.models.notification import Notification, NotificationStatus
from app.schemas.notification import NotificationCreate, NotificationResponse, NotificationList
from app.services.notification_service import NotificationService

router = APIRouter()
notification_service = NotificationService()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/notifications", response_model=NotificationResponse)
async def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db)
):
    """
    Create and send a new notification
    """
    db_notification = Notification(
        user_id=notification.user_id,
        type=notification.type,
        title=notification.title,
        content=notification.content,
        status=NotificationStatus.PENDING
    )
    
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    
    # Queue the notification for processing
    success = await notification_service.send_notification(db_notification)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to queue notification")
    
    return db_notification

@router.get("/users/{user_id}/notifications", response_model=NotificationList)
def get_user_notifications(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve all notifications for a specific user
    """
    notifications = (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    total = db.query(Notification).filter(Notification.user_id == user_id).count()
    
    return NotificationList(notifications=notifications, total=total)
