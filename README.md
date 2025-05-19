## Project Overview
A scalable notification service built with FastAPI that demonstrates the implementation of modern software development concepts including asynchronous programming, message queuing, and RESTful API design.

## Project Objectives
1. Implement a scalable notification system using modern Python frameworks
2. Demonstrate understanding of asynchronous programming concepts
3. Apply message queue patterns for distributed systems
4. Create a well-documented REST API with proper error handling
5. Practice proper software architecture and design patterns

## Technical Implementation

- Multiple notification channels:
  - Email notifications
  - SMS notifications
  - In-App notifications
- Asynchronous notification processing using RabbitMQ
- RESTful API with FastAPI
- SQLite database for notification storage
- Retry mechanism for failed notifications
- Real-time status tracking

## Prerequisites

- Python 3.8+
- Docker (for RabbitMQ)
- SMTP server access (for email notifications)

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update the configuration values in `.env`:
     - SMTP settings for email notifications
     - RabbitMQ connection details
     - Other service configurations

## Running the Service

1. Start RabbitMQ:
```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
```

2. Start the FastAPI server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

3. Start the notification worker:
```bash
python -m app.workers.notification_worker
```
### Send Notification
```http
POST /api/v1/notifications

{
    "user_id": 123,
    "type": "email",
    "title": "Welcome",
    "content": "Welcome to our service!"
}
```

### Get Notification Status
```http
GET /api/v1/notifications/{notification_id}
```

## Project Structure

```
app/
├── api/
│   └── v1/
│       └── endpoints/
│           └── notifications.py
├── core/
│   └── config.py
├── db/
│   └── base.py
├── models/
│   └── notification.py
├── schemas/
│   └── notification.py
├── services/
│   └── notification_service.py
├── workers/
│   └── notification_worker.py
└── main.py
```

## Configuration

The service can be configured using environment variables in the `.env` file:

- `PROJECT_NAME`: Name of the service
- `VERSION`: API version
- `API_V1_STR`: API version prefix
- `DATABASE_URL`: SQLite database connection URL
- `RABBITMQ_HOST`: RabbitMQ host
- `RABBITMQ_PORT`: RabbitMQ port
- `RABBITMQ_USER`: RabbitMQ username
- `RABBITMQ_PASS`: RabbitMQ password
- `SMTP_HOST`: SMTP server host
- `SMTP_PORT`: SMTP server port
- `SMTP_USER`: SMTP username
- `SMTP_PASSWORD`: SMTP password

## Learning Outcomes

Through this project, I have demonstrated competency in:

1. **FastAPI Framework**
   - Building RESTful APIs with modern Python
   - Implementing async/await patterns
   - API documentation using OpenAPI/Swagger

2. **Message Queue Systems**
   - RabbitMQ implementation
   - Asynchronous message processing
   - Distributed system architecture

3. **Database Management**
   - SQLAlchemy ORM usage
   - Database schema design
   - Data modeling best practices

4. **Software Architecture**
   - Clean code principles
   - Service-oriented architecture
   - Dependency injection patterns

5. **Error Handling & Logging**
   - Comprehensive error management
   - Status tracking and monitoring
   - Retry mechanisms for failed operations

## Challenges Faced and Solutions

1. **Asynchronous Processing**
   - Challenge: Managing concurrent notifications without blocking
   - Solution: Implemented RabbitMQ message queue for async processing

2. **Error Handling**
   - Challenge: Dealing with failed notifications
   - Solution: Created a retry mechanism with exponential backoff

3. **Scalability**
   - Challenge: Designing for high message volume
   - Solution: Implemented worker processes and message queuing

## Future Enhancements

1. Add support for push notifications
2. Implement rate limiting
3. Add message templates
4. Include analytics dashboard
5. Add support for webhook notifications

## Conclusion

This project demonstrates practical implementation of advanced Python concepts and modern software architecture patterns. The system is designed to be maintainable, scalable, and extensible for future enhancements.

## References

1. FastAPI Documentation: https://fastapi.tiangolo.com/
2. RabbitMQ Documentation: https://www.rabbitmq.com/documentation.html
3. SQLAlchemy Documentation: https://docs.sqlalchemy.org/
4. Python asyncio Documentation: https://docs.python.org/3/library/asyncio.html

---
Project submitted as part of the Advanced Programming with Python course requirements.