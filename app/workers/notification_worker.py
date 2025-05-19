import asyncio
import json
import logging
from typing import Optional
import aio_pika
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.base import SessionLocal
from app.models.notification import Notification, NotificationStatus
from app.services.notification_service import NotificationService

logger = logging.getLogger(__name__)

class NotificationWorker:
    def __init__(self):
        self.rabbitmq_url = f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASS}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}/"
        self.queue_name = "notifications"
        self.notification_service = NotificationService()
        self.max_retries = 3

    async def process_message(self, message: aio_pika.IncomingMessage, db: Session):
        async with message.process():
            try:
                # Parse message body
                body = json.loads(message.body.decode())
                notification_id = body["notification_id"]
                
                # Get notification from database
                notification = db.query(Notification).filter(Notification.id == notification_id).first()
                if not notification:
                    logger.error(f"Notification {notification_id} not found")
                    return

                # Process the notification
                success = await self.notification_service.process_notification(notification)
                
                if success:
                    notification.status = NotificationStatus.SENT
                else:
                    # Handle retry logic
                    if notification.retry_count < self.max_retries:
                        notification.retry_count += 1
                        notification.status = NotificationStatus.PENDING
                        # Requeue the message
                        await self.notification_service.send_notification(notification)
                    else:
                        notification.status = NotificationStatus.FAILED
                
                db.commit()

            except Exception as e:
                logger.error(f"Error processing message: {e}")
                db.rollback()

    async def run(self):
        # Connect to RabbitMQ
        connection = await aio_pika.connect_robust(self.rabbitmq_url)
        async with connection:
            # Create channel
            channel = await connection.channel()
            
            # Declare queue
            queue = await channel.declare_queue(
                self.queue_name,
                durable=True
            )
            
            logger.info("Starting notification worker...")
            
            # Process messages
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    db = SessionLocal()
                    try:
                        await self.process_message(message, db)
                    finally:
                        db.close()

async def main():
    worker = NotificationWorker()
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
