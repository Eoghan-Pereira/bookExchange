
from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    condition: Optional[str] = None
    isAvailable: bool = True
    description: Optional[str] = None
    userId: str
    image_url: str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: str

    class Config:
        from_attributes = True