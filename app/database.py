from pymongo.errors import PyMongoError
from models import Product, Category, UserCreate, UserResponse
from bson import ObjectId
from utils import is_valid_object_id, hash_password
from fastapi import HTTPException
from typing import List
from datetime import datetime
from conn_db import get_database_instance

# Instanciar la clase Database para manejar la conexión
db = get_database_instance()

# Verificar si categoria existe (insensible a mayúsculas/minúsculas)
def category_exists(category_name: str) -> bool:
    existing_category = db.categories_collection.find_one({"name": {"$regex": f"^{category_name}$", "$options": "i"}})
    return existing_category is not None

# Verificar si producto existe (insensible a mayúsculas/minúsculas)
def product_exists(product_name: str) -> bool:
    existing_product = db.products_collection.find_one({"name": {"$regex": f"^{product_name}$", "$options": "i"}})
    return existing_product is not None

# Verificar si usuario existe por eamil (insensible a mayúsculas/minúsculas)
def user_exists(user_email: str) -> bool:
    existing_user = db.users_collection.find_one({"email": {"$regex": f"^{user_email}$", "$options": "i"}})
    return existing_user is not None

# Verificar si la categoría tiene productos asociados
def category_has_products(category_id: str) -> bool:
    # Verificar si hay productos asociados a la categoría
    result = db.products_collection.find_one({"category_id": category_id})
    return result is not None

""" ------------- PRODUCT --------------- """
# Consultar productos con paginación
def get_paginated_products(page: int, page_size: int) -> List[Product]:
    # Calcular el desplazamiento (offset)
    offset = (page - 1) * page_size

    # Consultar la base de datos utilizando el offset y el tamaño de página
    products = list(db.products_collection.find({}).skip(offset).limit(page_size))
    # Convertir ObjectId a cadena y ajustar nombre de campo
    for product in products:
        product['id'] = str(product.pop('_id'))

    return [Product(**product) for product in products]

# Consultar producto por su id
def get_product_by_id(product_id: str) -> dict:
    product = db.products_collection.find_one({"_id": ObjectId(product_id)})
    if product:
        product['id'] = str(product.pop('_id'))  
        return product
    return None

# Consultar productos por categoria
def get_category_products(category_id: str) -> list:
    products = list(db.products_collection.find({"category_id": category_id}))
    for product in products:
        product['id'] = str(product.pop('_id')) 
    return products

# Crear producto
def create_product(product: Product):
    new_product = product.dict(exclude_unset=True)  # Excluir campos no configurados
    try:
        # Verificar si el producto ya existe por su nombre
        existing_product = db.products_collection.find_one({"name": new_product["name"]})
        if existing_product:
            return None  # O manejar como prefieras si el producto ya existe

        result = db.products_collection.insert_one(new_product)
        new_product_id = str(result.inserted_id)  # Obtener el ID como String
        new_product["_id"] = new_product_id  # Agregar el ID al producto creado
        return new_product  # Devuelve el producto creado con su ID como String
    except PyMongoError as e:
        # Manejar la excepción de MongoDB
        print(f"Error al insertar producto: {e}")
        return None

# Actualizar producto
def update_product(product_id: str, updated_data: dict):
    result = db.products_collection.update_one(
        {"_id": ObjectId(product_id)}, {"$set": updated_data})
    if result.modified_count > 0:
        return {"message": "Product updated"}
    elif result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        raise HTTPException(status_code=422, detail="Update operation failed")

# Eliminar producto
def delete_product(product_id: str):
    if not is_valid_object_id(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")

    result = db.products_collection.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count > 0:
        return {"message": "Product deleted"}
    elif result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        raise HTTPException(
            status_code=422, detail="Deletion operation failed")
        
""" ------------- CATEGORY --------------- """
# Consultar categorias
def get_categories() -> list:
    categories = list(db.categories_collection.find({}))
    return [Category(**{**category, "id": str(category.pop("_id"))}) for category in categories]

# Consultar categoria por su id
def get_category_by_id(category_id: str) -> dict:
    category = db.categories_collection.find_one({"_id": ObjectId(category_id)})
    if category:
        category['id'] = str(category.pop('_id'))  
        return category
    return None

# Crear categoria
def create_category(category: Category):
    new_category = category.dict(exclude_unset=True)  # Excluir campos no configurados
    try:
        # Verificar si la categoría ya existe por su nombre
        existing_category = db.categories_collection.find_one({"name": new_category["name"]})
        if existing_category:
            return None  # O manejar como prefieras si la categoría ya existe

        result = db.categories_collection.insert_one(new_category)
        new_category_id = str(result.inserted_id)  # Obtener el ID como String
        new_category["_id"] = new_category_id  # Agregar el ID a la categoría creada
        return new_category  # Devuelve la categoría creada con su ID como String
    except PyMongoError as e:
        # Manejar la excepción de MongoDB
        print(f"Error al insertar categoría: {e}")
        return None

# Actualizar categoria
def update_category(category_id: str, updated_data: dict):
    result = db.categories_collection.update_one(
        {"_id": ObjectId(category_id)}, {"$set": updated_data})
    if result.modified_count > 0:
        return {"message": "Category updated"}
    elif result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    else:
        raise HTTPException(status_code=422, detail="Update operation failed")

# Eliminar categoria
def delete_category(category_id: str):
    if not is_valid_object_id(category_id):
        raise HTTPException(status_code=400, detail="Invalid category ID")

    result = db.categories_collection.delete_one({"_id": ObjectId(category_id)})
    if result.deleted_count > 0:
        return {"message": "Category deleted"}
    elif result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    else:
        raise HTTPException(
            status_code=422, detail="Deletion operation failed")

""" ------------- USER --------------- """
# Crear usuario
def create_user(user: UserCreate):
    new_user = user.dict(exclude_unset=True)  # Excluir campos no configurados
    new_user['avatar'] = str(new_user['avatar'])  # Convertir la URL a una cadena
    new_user['created_at'] = str(datetime.utcnow())
    new_user['updated_at'] = str(datetime.utcnow())
    
    # Excluir el campo 'confirm_password' antes de la inserción
    new_user.pop('confirm_password', None)
    
    # Hashear la contraseña antes de guardarla en la base de datos
    hashed_password = hash_password(user.password)
    new_user['password'] = hashed_password
    
    try:
        # Verificar si el usuario ya existe por su email
        existing_user = db.users_collection.find_one({"email": new_user["email"]})
        if existing_user:
            return None  

        result = db.users_collection.insert_one(new_user)
        new_user_id = str(result.inserted_id)  # Obtener el ID como String
        new_user["_id"] = new_user_id  # Agregar el ID al usuario creado
        return new_user  
    except PyMongoError as e:
        # Manejar la excepción de MongoDB
        print(f"Error al insertar usuario: {e}")
        return None

# Consultar usuario por su id
def get_user_by_id(user_id: str) -> dict:
    try:
        user = db.users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user['id'] = str(user.pop('_id'))  
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        # Manejar otros errores, como errores de conexión, etc.
        raise HTTPException(status_code=500, detail=f"Error retrieving user: {e}")

# Consultar usuario por su nombre de usuario
async def get_user_by_username(username: str) -> dict:
    return await db.users_collection.find_one({"username": username})

# Consultar usuario por su email
async def get_user_by_email(email: str) -> dict:
    return await db.users_collection.find_one({"email": email})

# Actualizar usuario
async def update_user(user_id: str, updated_data: dict) -> bool:
    updated_data['updated_at'] = datetime.utcnow()
    result = await db.users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_data})
    return result.modified_count > 0

# Eliminar usuario
async def delete_user(user_id: str) -> bool:
    result = await db.users_collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count > 0

# Cerrar la conexión
db.close_connection()