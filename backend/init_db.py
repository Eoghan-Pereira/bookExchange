from flask import Flask
from services.mongodb_service import mongo, init_db
from datetime import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/bookexchange"

def setup_sample_data():
    try:
        # Clear existing data
        mongo.db.books.delete_many({})
        mongo.db.transactions.delete_many({})

        # Insert sample books
        sample_books = [
            {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "genre": "Fiction",
                "condition": "Good",
                "user_id": "user1",
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "title": "1984",
                "author": "George Orwell",
                "genre": "Science Fiction",
                "condition": "Excellent",
                "user_id": "user2",
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            }
        ]
        mongo.db.books.insert_many(sample_books)
        print("Sample data inserted successfully")
        return True
    except Exception as e:
        print(f"Error setting up sample data: {e}")
        return False

if __name__ == "__main__":
    if init_db(app):
        setup_sample_data()
        print("Database initialized successfully")
    else:
        print("Database initialization failed")
