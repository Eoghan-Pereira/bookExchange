from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query, Body, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from services.mongodb_service import get_all_books, add_book, get_user_books, update_book, delete_book
import base64

router = APIRouter()
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
security = HTTPBearer()

def allowed_file(filename: str):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@router.get("/books")
async def get_books(
    search: str = Query(None, description="Search by title or author"),
    genre: str = Query(None, description="Filter by genre")
):
    try:
        # Build query filters
        query = {}
        if search:
            # Case-insensitive search in title or author
            query["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"author": {"$regex": search, "$options": "i"}}
            ]
        if genre:
            query["genre"] = {"$regex": f"^{genre}$", "$options": "i"}

        books = await get_all_books(query)
        return {"books": [book for book in books if book and '_id' in book]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/books")
async def create_book(
    image: UploadFile = File(...),
    title: str = Form(...),
    author: str = Form(...),
    genre: str = Form(...),
    condition: Optional[str] = Form(None),
    isAvailable: bool = Form(True),
    description: Optional[str] = Form(None),
    userId: str = Form(...),
):
    try:
        if not image.filename:
            raise HTTPException(status_code=400, detail="No file provided")

        # Read the image file and convert it to a base64 string
        image_data = await image.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')

        book_data = {
            "title": title,
            "author": author,
            "genre": genre,
            "condition": condition,
            "isAvailable": isAvailable,
            "description": description,
            "userId": userId,
            "image_base64": image_base64,
        }

        result = await add_book(book_data)
        return {"message": "Book added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/books/{user_id}")
async def list_books(user_id: str):
    books = await get_user_books(user_id)
    return books

@router.post("/upload")
async def upload_file(image: UploadFile = File(...)):
    if not image.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    if not allowed_file(image.filename):
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Read the image file and convert it to a base64 string
    image_data = await image.read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')

    return {"image_base64": image_base64}

@router.put("/books/{book_id}")
async def update_book_endpoint(
    book_id: str,
    book_data: dict = Body(...),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        # Remove _id from update data if present
        if '_id' in book_data:
            del book_data['_id']
            
        updated = await update_book(book_id, book_data)
        if not updated:
            raise HTTPException(status_code=404, detail="Book not found")
        return {"message": "Book updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/books/{book_id}")
async def delete_book_endpoint(
    book_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        # Add auth validation here if needed
        deleted = await delete_book(book_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Book not found")
        return {"message": "Book deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))