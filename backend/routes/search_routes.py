# routes/search_routes.py
from flask import Blueprint, request, jsonify
from services.mongodb_service import mongo

search_routes = Blueprint("search", __name__)

@search_routes.route("/search", methods=["GET"])
def search_books():
    query = request.args
    filters = {key: value for key, value in query.items() if value}
    books = mongo.db.books.find(filters)
    return jsonify([book for book in books]), 200
