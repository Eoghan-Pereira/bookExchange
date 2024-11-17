# routes/transaction_routes.py
from flask import Blueprint, request, jsonify, current_app
from services.mongodb_service import db
from bson import ObjectId
from datetime import datetime

transaction_routes = Blueprint("transactions", __name__)

@transaction_routes.route("/transactions/<user_id>", methods=["GET"])
async def list_transactions(user_id):
    try:
        transactions = await db.transactions.find({
            "$or": [
                {"requesterId": user_id},
                {"ownerId": user_id}
            ]
        }).sort("createdAt", -1).to_list(length=None)
        
        return jsonify([{
            **transaction,
            "_id": str(transaction["_id"])
        } for transaction in transactions]), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching transactions: {e}")
        return jsonify({"error": "Failed to fetch transactions"}), 500

@transaction_routes.route("/transactions", methods=["POST"])
async def create_transaction():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        data["createdAt"] = datetime.utcnow()
        data["status"] = "pending"
        
        result = await db.transactions.insert_one(data)
        return jsonify({
            "message": "Transaction created successfully",
            "id": str(result.inserted_id)
        }), 201
    except Exception as e:
        current_app.logger.error(f"Error creating transaction: {e}")
        return jsonify({"error": "Failed to create transaction"}), 500
