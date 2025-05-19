from typing import Optional
from app.models.notification import Notification, NotificationType, NotificationStatus
from app.core.config import settings
import aio_pika
import json
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        self.rabbitmq_url = f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASS}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}/"
        self.queue_name = "notifications"

    async def send_notification(self, notification: Notification) -> bool:
        """
        Queue a notification for processing
        """
        try:
            # Connect to RabbitMQ
            connection = await aio_pika.connect_robust(self.rabbitmq_url)
            async with connection:
                channel = await connection.channel()
                
                # Declare the queue
                queue = await channel.declare_queue(
                    self.queue_name,
                    durable=True
                )

                # Convert notification to dict for serialization
                message_body = {
                    "notification_id": notification.id,
                    "type": notification.type,
                    "user_id": notification.user_id,
                    "title": notification.title,
                    "content": notification.content,
                    "retry_count": notification.retry_count
                }

                # Publish message
                await channel.default_exchange.publish(
                    aio_pika.Message(
                        body=json.dumps(message_body).encode(),
                        delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                    ),
                    routing_key=self.queue_name,
                )

                return True
        except Exception as e:
            logger.error(f"Error queuing notification: {e}")
            return False

    async def process_notification(self, notification: Notification) -> bool:
        """
        Process a notification based on its type
        """
        try:
            if notification.type == NotificationType.EMAIL:
                # Implement email sending logic here
                success = await self._send_email(notification)
            elif notification.type == NotificationType.SMS:
                # Implement SMS sending logic here
                success = await self._send_sms(notification)
            elif notification.type == NotificationType.IN_APP:
                # In-app notifications are already stored in DB
                success = True
            
            return success
        except Exception as e:
            logger.error(f"Error processing notification: {e}")
            return False

    async def _send_email(self, notification: Notification) -> bool:
        """
        Simulate sending an email
        In a real implementation, you would use SMTP or an email service
        """
        try:
            logger.info(f"Sending email to user {notification.user_id}: {notification.title}")
            # Implement actual email sending logic here
            return True
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False

    async def _send_sms(self, notification: Notification) -> bool:
        """
        Simulate sending an SMS
        In a real implementation, you would use Twilio or another SMS service
        """
        try:
            logger.info(f"Sending SMS to user {notification.user_id}: {notification.title}")
            # Implement actual SMS sending logic here
            return True
        except Exception as e:
            logger.error(f"Error sending SMS: {e}")
            return False
