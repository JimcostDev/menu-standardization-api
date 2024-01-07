from pydantic import BaseModel, Field, constr, validator, EmailStr, HttpUrl
from typing import List, Optional

# ------------------ PRODUCT ----------------
class ProductBase(BaseModel):
    name: constr(min_length=1, max_length=100) = Field(..., description="El nombre del producto.")
    description: constr(min_length=1, max_length=300) = Field(..., description="Una breve descripción del producto.")
    category_id: constr(min_length=24, max_length=24) = Field(..., description="ID de la categoría a la que pertenece el producto.")
    tags: List[str] = Field(..., description="Etiquetas asociadas al producto, como 'vegano', 'sin gluten', etc.")
    price: float = Field(..., gt=0, description="El precio del producto, debe ser mayor que 0.")
    image: str = Field(..., description="URL de la imagen del producto")

    @validator('tags')
    def validate_tags(cls, v):
        if len(v) < 1 or len(v) > 10:
            raise ValueError('Debe haber entre 1 y 10 etiquetas')
        return v   

    class Config:
        from_attributes = True

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: Optional[str] = Field(None, description="ID del producto")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Torta de Chocolate",
                "description": "Una deliciosa torta de chocolate con capas de crema y cerezas.",
                "category_id": "617bf036038995294e3c7c4f",
                "tags": ["dulce", "chocolate", "sin gluten"],
                "price": 19.99,
                "image": "https://example.com/torta.jpg"
            }
        }

# ------------------ CATEGORY ----------------
class Category(BaseModel):
    name: constr(min_length=1, max_length=100) = Field(..., description="El nombre de la categoría.")
    image: str = Field(..., description="URL de la imagen de la categoría")
    id: Optional[str] = Field(None, description="ID de la categoría")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Postres",
                "image": "https://example.com/postres.jpg"
            }
        }


# ------------------ USER ----------------
class GoogleInfo(BaseModel):
    google_id: str = Field(..., description="ID proporcionado por Google")
    access_token: str = Field(..., description="Token de acceso de Google")
    refresh_token: str = Field(..., description="Token de actualización de Google")
    # Otros campos relevantes proporcionados por Google

class ResetToken(BaseModel):
    token: str = Field(..., description="Token de reinicio para el usuario.")
    expires_at: str = Field(..., description="Fecha de vencimiento del token de reinicio.")

    class Config:
        json_schema_extra = {
            "example": {
                "token": "reset_token_123",
                "expires_at": "2025-01-01T00:00:00"
            }
        }
    
class UserBase(BaseModel):
    """Schema for creating a User."""
    username: constr(min_length=4, max_length=50) = Field(..., description="Nombre de usuario (entre 4 y 50 caracteres)")
    email: EmailStr = Field(..., description="Dirección de correo electrónico")
    password: constr(min_length=8)
    confirm_password: constr(min_length=8)
    avatar: HttpUrl = Field(..., description="URL de la imagen o avatar del usuario")
    roles: List[str] = Field(default_factory=lambda: ["user"], description="Lista de roles del usuario")
    google_info: Optional[GoogleInfo] = Field(None, description="Información opcional proporcionada por Google")
    reset_tokens: Optional[List[ResetToken]] = Field(None, description="Tokens de reinicio para el usuario")
    
    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Las contraseñas no coinciden')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('La contraseña debe contener al menos una letra mayúscula')
        if not any(c.islower() for c in v):
            raise ValueError('La contraseña debe contener al menos una letra minúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('La contraseña debe contener al menos un número')
        if not any(c in '!@#$%^&*:' for c in v):
            raise ValueError('La contraseña debe contener al menos un carácter especial')
        return v

class UserCreate(UserBase):
    pass

class UserResponse(BaseModel):
    """Schema for User response."""
    id: Optional[str] = Field(None, description="ID del usuario")
    username: constr(min_length=4, max_length=50) = Field(..., description="Nombre de usuario (entre 4 y 50 caracteres)")
    email: EmailStr = Field(..., description="Dirección de correo electrónico")
    avatar: HttpUrl = Field(..., description="URL de la imagen o avatar del usuario")
    roles: List[str] = Field(default_factory=lambda: ["user"], description="Lista de roles del usuario")
class UserInDB(UserResponse):
    """Schema for User stored in database."""
    created_at: str = Field(..., description="Fecha de creación del usuario")
    updated_at: str = Field(..., description="Fecha de última actualización del usuario")
