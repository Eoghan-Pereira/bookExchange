# services/mongodb_service.py
from motor.motor_asyncio import AsyncIOMotorClient
from config import Config
from bson import ObjectId
import json
from datetime import datetime
from typing import Optional

class MongoDBService:
    def __init__(self, mongo_url: str):
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client.book_exchange
        self.exchanges = self.db.exchanges
        self.notifications = self.db.notifications

    async def init_db(self):
        self.client = AsyncIOMotorClient(Config.MONGO_URI)
        self.db = self.client[Config.MONGODB_DB]
        return True

    def convert_mongodb_doc(self, doc):
        if doc is None:
            return None
        doc['_id'] = str(doc.get('_id', ''))  # Handle cases where _id might not exist
        return {k: v for k, v in doc.items() if v is not None}  # Remove None values

    async def get_user_books(self, user_id: str):
        cursor = self.db.books.find({"userId": user_id})
        books = await cursor.to_list(length=None)
        return [self.convert_mongodb_doc(book) for book in books]

    async def add_book(self, book_data: dict):
        try:
            result = await self.db.books.insert_one(book_data)
            return str(result.inserted_id)
        except Exception as e:
            raise e

    async def get_all_books(self, query=None):
        try:
            if query is None:
                query = {}
            cursor = self.db.books.find(query)
            books = await cursor.to_list(length=100)
            # Convert ObjectId to string for JSON serialization
            for book in books:
                book['_id'] = str(book['_id'])
            return books
        except Exception as e:
            print(f"Error fetching books: {e}")
            return []

    async def get_user_exchanges(self, user_id: str):
        cursor = self.db.exchanges.find({
            "$or": [
                {"requesterId": user_id},
                {"ownerId": user_id}
            ]
        }).sort("createdAt", -1)
        exchanges = await cursor.to_list(length=None)
        return [self.convert_mongodb_doc(ex) for ex in exchanges]

    async def get_exchange(self, exchange_id: str):
        exchange = await self.db.exchanges.find_one({"_id": ObjectId(exchange_id)})
        return self.convert_mongodb_doc(exchange)

    async def create_exchange(self, exchange_data: dict):
        exchange_data["createdAt"] = datetime.utcnow()
        result = await self.db.exchanges.insert_one(exchange_data)
        return str(result.inserted_id)

    async def update_exchange_status(self, exchange_id: str, status: str):
        result = await self.db.exchanges.update_one(
            {"_id": ObjectId(exchange_id)},
            {
                "$set": {
                    "status": status,
                    "updatedAt": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0

    async def get_available_books(self):
        try:
            cursor = self.db.books.find({"isAvailable": True})
            books = await cursor.to_list(length=None)
            print("Raw books from DB:", books)  # Debug log
            
            converted_books = []
            for book in books:
                book_dict = self.convert_mongodb_doc(book)
                book_dict['id'] = book_dict.pop('_id')  # Convert _id to id
                converted_books.append(book_dict)
            
            print("Converted books:", converted_books)  # Debug log
            return converted_books
        except Exception as e:
            print(f"Error in get_available_books: {e}")
            raise e

    async def create_exchange_request(self, exchange: dict):
        result = await self.exchanges.insert_one(exchange)
        return str(result.inserted_id)

    async def get_exchange_requests(self, user_id: str, status: Optional[str] = None):
        query = {
            "$or": [
                {"requester_id": user_id},
                {"recipient_id": user_id}
            ]
        }
        if status:
            query["status"] = status
        cursor = self.exchanges.find(query)
        return await cursor.to_list(length=None)

    async def update_exchange_status(self, exchange_id: str, status: str, modified_terms: Optional[dict] = None):
        update_data = {
            "$set": {
                "status": status,
                "modified_at": datetime.utcnow()
            }
        }
        if modified_terms:
            update_data["$set"].update(modified_terms)
        
        result = await self.exchanges.update_one(
            {"_id": ObjectId(exchange_id)},
            update_data
        )
        return result.modified_count > 0

    async def create_notification(self, user_id: str, message: str, type: str, reference_id: str):
        notification = {
            "user_id": user_id,
            "message": message,
            "type": type,
            "reference_id": reference_id,
            "created_at": datetime.utcnow(),
            "read": False
        }
        await self.notifications.insert_one(notification)

    async def update_book(self, book_id: str, book_data: dict):
        result = await self.db.books.update_one(
            {"_id": ObjectId(book_id)},
            {"$set": book_data}
        )
        return result.modified_count > 0

    async def delete_book(self, book_id: str):
        result = await self.db.books.delete_one({"_id": ObjectId(book_id)})
        return result.deleted_count > 0

# Create singleton instance
mongo_service = MongoDBService(Config.MONGO_URI)

# Initialize database
async def init_db():
    return await mongo_service.init_db()

# Export wrapper functions
async def get_all_books(query=None):
    return await mongo_service.get_all_books(query)

async def add_book(book_data: dict):
    return await mongo_service.add_book(book_data)

async def get_user_books(user_id: str):
    return await mongo_service.get_user_books(user_id)

async def update_book(book_id: str, book_data: dict):
    return await mongo_service.update_book(book_id, book_data)

async def delete_book(book_id: str):
    return await mongo_service.delete_book(book_id)

# Update exports
__all__ = [
    'MongoDBService',
    'mongo_service',
    'init_db',
    'get_all_books',
    'add_book',
    'get_user_books',
    'update_book',
    'delete_book'
]
