from pydantic import BaseModel, Field, HttpUrl, ConfigDict, StringConstraints
from typing import List, Optional, Annotated

# Modelo para la categoría
class Category(BaseModel):
    id: Optional[str] = Field(None, alias="_id", description="ID de la categoría")
    name: Annotated[str, StringConstraints(min_length=1, max_length=50)] = Field(
        ..., description="Nombre de la categoría"
    )
    image: HttpUrl = Field(..., description="URL de la imagen de la categoría")

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "_id": "60d5ec49f87d2e5a2c9c1234",
                "name": "Postres",
                "image": "https://example.com/category.jpg"
            }
        }
    )

# Modelo base para Producto
class ProductBase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "name": "Torta de Chocolate",
                "description": "Una deliciosa torta de chocolate con capas de crema y cerezas.",
                "category": {
                    "_id": "60d5ec49f87d2e5a2c9c1234",
                    "name": "Postres",
                    "image": "https://example.com/category.jpg"
                },
                "tags": ["dulce", "sin gluten"],
                "price": 19.99,
                "image": "https://api.lorem.space/image/fashion?w=150&h=150"
            }
        }
    )

    name: Annotated[str, StringConstraints(min_length=1, max_length=100)] = Field(
        ..., description="El nombre del producto."
    )
    description: Annotated[str, StringConstraints(min_length=1, max_length=300)] = Field(
        ..., description="Una breve descripción del producto."
    )
    category: Category = Field(..., description="La categoría a la que pertenece el producto")
    tags: Annotated[List[str], Field(min_length=1, max_length=10)] = Field(
        ..., description="Etiquetas asociadas al producto (1-10 etiquetas)"
    )
    price: float = Field(..., gt=0, description="Precio mayor que 0.")
    image: HttpUrl = Field(..., description="URL válida de la imagen del producto")

# Modelo para la creación de un producto (se hereda de ProductBase)
class ProductCreate(ProductBase):
    pass

# Modelo para la respuesta, donde se incluye el ID del producto (alias para _id)
class ProductResponse(ProductBase):
    id: Optional[str] = Field(None, alias="_id", description="ID del producto")
    
class ProductUpdate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "name": "Torta de Chocolate Mejorada",
                "description": "Actualización: Torta con más crema.",
                "category": {
                    "_id": "60d5ec49f87d2e5a2c9c1234",
                    "name": "Postres",
                    "image": "https://example.com/category.jpg"
                },
                "tags": ["dulce"],
                "price": 21.99,
                "image": "https://api.lorem.space/image/fashion?w=150&h=150"
            }
        }
    )

    name: Optional[Annotated[str, StringConstraints(min_length=1, max_length=100)]] = Field(
        None, description="El nombre del producto."
    )
    description: Optional[Annotated[str, StringConstraints(min_length=1, max_length=300)]] = Field(
        None, description="Una breve descripción del producto."
    )
    category: Optional['Category'] = Field(
        None, description="La categoría a la que pertenece el producto"
    )
    tags: Optional[Annotated[List[str], Field(min_length=1, max_length=10)]] = Field(
        None, description="Etiquetas asociadas al producto (1-10 etiquetas)"
    )
    price: Optional[float] = Field(None, gt=0, description="Precio mayor que 0.")
    image: Optional[HttpUrl] = Field(None, description="URL válida de la imagen del producto")
