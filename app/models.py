from pydantic import BaseModel, Field, constr, validator
from typing import List

class Product(BaseModel):
    name: constr(min_length=1, max_length=100) = Field(..., description="El nombre del producto.")
    description: constr(min_length=1, max_length=300) = Field(..., description="Una breve descripción del producto.")
    category: constr(min_length=1, max_length=100) = Field(..., description="La categoría a la que pertenece el producto.")
    tags: List[str] = Field(..., description="Etiquetas asociadas al producto, como 'vegano', 'sin gluten', etc.")
    price: float = Field(..., gt=0, description="El precio del producto, debe ser mayor que 0.")

    @validator('tags')
    def validate_tags(cls, v):
        if len(v) < 1 or len(v) > 10:
            raise ValueError('Debe haber entre 1 y 10 etiquetas')
        return v

    class Config:
        schema_extra = {
            "example": {
                "name": "Torta de Chocolate",
                "description": "Una deliciosa torta de chocolate con capas de crema y cerezas.",
                "category": "Postres",
                "tags": ["dulce", "chocolate", "sin gluten"],
                "price": 19.99
            }
        }


class Category(BaseModel):
    name: constr(min_length=1, max_length=100) = Field(..., description="El nombre de la categoría.")

    class Config:
        schema_extra = {
            "example": {
                "name": "Postres"
            }
        }
