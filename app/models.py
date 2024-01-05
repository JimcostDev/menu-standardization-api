from pydantic import BaseModel, Field, constr, validator
from typing import List

class Product(BaseModel):
    id: str = Field(..., description="ID del producto")
    name: constr(min_length=1, max_length=100) = Field(...,
                                                       description="El nombre del producto.")
    description: constr(min_length=1, max_length=300) = Field(...,
                                                              description="Una breve descripción del producto.")
    
    category_id: constr(min_length=24, max_length=24) = Field(..., 
                                                              description="ID de la categoría a la que pertenece el producto.")
    
    tags: List[str] = Field(
        ..., description="Etiquetas asociadas al producto, como 'vegano', 'sin gluten', etc.")
    
    price: float = Field(..., gt=0,
                         description="El precio del producto, debe ser mayor que 0.")
    image: str = Field(..., description="URL de la imagen del producto")  
    

    @validator('tags')
    def validate_tags(cls, v):
        if len(v) < 1 or len(v) > 10:
            raise ValueError('Debe haber entre 1 y 10 etiquetas')
        return v   

    class Config:
        schema_extra = {
            "example": {
                "_id": "617bf036038995294e3c7c4f",
                "name": "Torta de Chocolate",
                "description": "Una deliciosa torta de chocolate con capas de crema y cerezas.",
                "category_id": "617bf036038995294e3c7c4f",
                "tags": ["dulce", "chocolate", "sin gluten"],
                "price": 19.99,
                "image": "https://example.com/torta.jpg"
            }
        }

class Category(BaseModel):
    id: str = Field(..., description="ID de la categoría")
    name: constr(min_length=1, max_length=100) = Field(...,
                                                       description="El nombre de la categoría.")
    image: str = Field(..., description="URL de la imagen de la categoría")

    class Config:
        schema_extra = {
            "example": {
                "_id": "617bf036038995294e3c7c4f",
                "name": "Postres",
                "image": "https://example.com/postres.jpg"
            }
        }
