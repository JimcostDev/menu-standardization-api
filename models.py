from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    name: str
    description: str
    category: str
    tags: List[str]
    price: float

class Category(BaseModel):
    name: str
