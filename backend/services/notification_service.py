
from typing import Optional
from datetime import datetime
from services.mongodb_service import db

async def create_notification(user_id: str, message: str, type: str, exchange_id: Optional[str] = None):
    notification = {
        "userId": user_id,
        "message": message,
        "type": type,
        "exchangeId": exchange_id,
        "createdAt": datetime.utcnow(),
        "read": False
    }
    return await db.notifications.insert_one(notification)

async def notify_exchange_status(exchange_id: str, status: str, owner_id: str, requester_id: str):
    message = f"Exchange request has been {status}"
    await create_notification(owner_id, message, "exchange_status", exchange_id)
    await create_notification(requester_id, message, "exchange_status", exchange_id)

async def get_user_notifications(user_id: str):
    return await db.notifications.find({"userId": user_id}).sort("createdAt", -1).to_list(None)