import os
import math
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import base64
from services.mongodb_service import get_all_books, add_book, get_user_books, get_books_count

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

router = APIRouter()

@router.get("/books")
async def get_books(page: int = 1, limit: int = 12):
    skip = (page - 1) * limit
    total_books = await get_books_count()
    books = await get_all_books(skip=skip, limit=limit)
    
    return {
        "books": books,
        "total": total_books,
        "page": page,
        "pages": math.ceil(total_books / limit)
    }

@router.post("/books")
async def create_book(
    image: UploadFile = File(...),
    title: str = Form(...),
    author: str = Form(...),
    genre: str = Form(...),
    condition: str = Form(...),
    description: Optional[str] = Form(None),
    isAvailable: bool = Form(True),
    userId: str = Form(...)
):
    try:
        if not image.filename or not allowed_file(image.filename):
            raise HTTPException(status_code=400, detail="Invalid file type")

        # Create unique filename
        filename = f"{userId}_{image.filename}"
        
        # Ensure upload directory exists
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Save the file
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        contents = await image.read()
        with open(file_path, 'wb') as f:
            f.write(contents)

        # Prepare book data
        book_data = {
            'title': title,
            'author': author,
            'genre': genre,
            'condition': condition,
            'isAvailable': isAvailable,
            'description': description,
            'userId': userId,
            'image_url': f'/uploads/{filename}'
        }

        # Add to database
        result = await add_book(book_data)
        return JSONResponse(
            content={"message": "Book added successfully", "book": result},
            status_code=201
        )

    except Exception as e:
        print(f"Error creating book: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/books/{user_id}")
async def list_books(user_id: str):
    books = await get_user_books(user_id)
    return books

# Remove Flask-specific routes
