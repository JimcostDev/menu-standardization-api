from pymongo.errors import PyMongoError
from models import Product, Category, UserCreate, UserUpdate
from bson import ObjectId
from utils import is_valid_object_id, hash_password
from fastapi import HTTPException, status
from typing import List
from datetime import datetime
from conn_db import get_database_instance
import re

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
    new_user['roles'] = ['user']
    
    # Excluir el campo 'confirm_password' antes de la inserción
    new_user.pop('confirm_password', None)
    
    # Hashear la contraseña antes de guardarla en la base de datos
    hashed_password = hash_password(user.password)
    new_user['password'] = hashed_password
    
    try:
        # Verificar si el usuario ya existe por su email
        if user_exists(new_user['email']):
            return None, status.HTTP_409_CONFLICT  # Retorna None con un código de conflicto si el usuario ya existe

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
    except Exception as e:
        # Manejar otros errores, como errores de conexión, etc.
        raise HTTPException(status_code=500, detail=f"Error retrieving user: {e}")

# Consultar usuario por su email
def get_user_by_email(user_email: str) -> dict:
    try:
        user = db.users_collection.find_one({"email": user_email})
        if user:
            user['id'] = str(user.pop('_id'))  
            return user
    except Exception as e:
        # Manejar otros errores, como errores de conexión, etc.
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error retrieving user: {e}")

# Consultar usuarios con usernames similares
def get_users(user_name: str) -> list:
    try:
        # Crear una expresión regular para buscar usernames similares
        regex = re.compile(f".*{re.escape(user_name)}.*", re.IGNORECASE)

        # Realizar la búsqueda en la base de datos utilizando la expresión regular
        users = list(db.users_collection.find({"username": regex}))

        for user in users:
           user['id'] = str(user.pop('_id')) 

        return users
    except Exception as e:
        # Manejar otros errores, como errores de conexión, etc.
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error retrieving users: {e}")

# Actualizar usuario    
def update_user(user_id: str, updated_info: UserUpdate):
    existing_user = get_user_by_id(user_id)
    
    if existing_user is None:
        return None, status.HTTP_404_NOT_FOUND

    # Verificar si el email actualizado ya existe en otro usuario
    if updated_info.email != existing_user['email']:
        if user_exists(updated_info.email):
            return None, status.HTTP_409_CONFLICT  # Email ya existe en otro usuario
    
    try:
        updated_values = updated_info.dict(exclude_unset=True)
        updated_values['updated_at'] = str(datetime.utcnow())
        updated_values['avatar'] = str(updated_values['avatar'])
        # Excluir el campo 'confirm_password' antes de la inserción
        updated_values.pop('confirm_password', None)
    
        # Hashear la contraseña si se actualiza
        if 'password' in updated_values:
            hashed_password = hash_password(updated_values['password'])
            updated_values['password'] = hashed_password

        db.users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": updated_values}
        )

        updated_user = get_user_by_id(user_id)
        return updated_user, status.HTTP_200_OK
    except PyMongoError as e:
        print(f"Error al actualizar usuario: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al actualizar usuario")

# Eliminar usuario
def delete_user(user_id: str) -> bool:
    try:
        # Consulta el usuario por su ID antes de eliminarlo
        user = db.users_collection.find_one({"_id": ObjectId(user_id)})
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró el usuario para eliminar")
        
        # Verifica el rol del usuario
        user_roles = user.get("roles", [])
        
        if "super-admin" in user_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No se puede eliminar un usuario con rol 'super-admin', si quieres eliminar este usuario, cambia su rol.")
        
        # Procede con la eliminación si el rol no es 'super-admin'
        result = db.users_collection.delete_one({"_id": ObjectId(user_id)})
        
        if result.deleted_count > 0:
            return True
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró el usuario para eliminar")
    
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al eliminar usuario: {e}")

# Cerrar la conexión
db.close_connection()