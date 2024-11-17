# routes/auth_routes.py
from flask import Blueprint, request, jsonify
from services.firebase_service import verify_token

auth_routes = Blueprint("auth", __name__)

@auth_routes.route("/auth/verify", methods=["POST"])
def verify_user():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token missing"}), 401
    user = verify_token(token)
    if user:
        return jsonify({"user": user}), 200
    return jsonify({"error": "Invalid token"}), 403
