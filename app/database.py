from pymongo import MongoClient, TEXT
from pymongo.errors import PyMongoError
from models import Product, Category
from bson import ObjectId
from utils import is_valid_object_id
from fastapi import HTTPException
import os
from dotenv import load_dotenv
from typing import List

# Obtiene la cadena de conexión desde config.env
load_dotenv("config.env")
mongo_uri = os.getenv("MONGO_URI")

# Conexión a MongoDB
client = MongoClient(mongo_uri)
#client = MongoClient('mongodb://localhost:27017/')
db = client['api_menu_db']

# Colecciones en la base de datos
products_collection = db['products']
categories_collection = db['categories']

# Operaciones en la base de datos

# Crear un índice de texto en los campos 'name' de las colecciones para consultas insensibles a mayúsculas/minúsculas
categories_collection.create_index([("name", TEXT)])
products_collection.create_index([("name", TEXT)])

# Verificar si categoria existe (insensible a mayúsculas/minúsculas)
def category_exists(category_name: str) -> bool:
    existing_category = categories_collection.find_one({"name": {"$regex": f"^{category_name}$", "$options": "i"}})
    return existing_category is not None

# Verificar si producto existe (insensible a mayúsculas/minúsculas)
def product_exists(product_name: str) -> bool:
    existing_product = products_collection.find_one({"name": {"$regex": f"^{product_name}$", "$options": "i"}})
    return existing_product is not None

# Verificar si la categoría tiene productos asociados
def category_has_products(category_id: str) -> bool:
    # Verificar si hay productos asociados a la categoría
    result = products_collection.find_one({"category_id": category_id})
    return result is not None

# ***************** CRUD ************* #
# GETS
def get_categories() -> list:
    return list(categories_collection.find({}, {"_id": 0}))

def get_category_products(category_id: str) -> list:
    return list(products_collection.find({"category_id": category_id}, {"_id": 0}))

# Consultar los productos con paginación
def get_paginated_products(page: int, page_size: int) -> List[Product]:
    # Calcular el desplazamiento (offset)
    offset = (page - 1) * page_size

    # Consultar la base de datos utilizando el offset y el tamaño de página
    products = list(products_collection.find({}, {"_id": 0}).skip(offset).limit(page_size))

    return products

def get_product_by_id(product_id: str) -> dict:
    product = products_collection.find_one(
        {"_id": ObjectId(product_id)}, {"_id": 0})
    if product:
        return product
    return None  # Opcional: también puedes devolver un objeto vacío o lanzar una excepción

def get_category_by_id(category_id: str) -> dict:
    category = categories_collection.find_one(
        {"_id": ObjectId(category_id)}, {"_id": 0})
    if category:
        return category
    return None  # Opcional: también puedes devolver un objeto vacío o lanzar una excepción

# CREATES
def create_category(category: Category):
    new_category = category.dict()
    try:
        # Verificar si la categoría ya existe
        if categories_collection.find_one({"name": new_category["name"]}):
            return None  # O manejar como prefieras

        result = categories_collection.insert_one(new_category)
        new_category_id = result.inserted_id
        new_category["_id"] = str(new_category_id)  # Convierte ObjectId a String
        return new_category  # Devuelve la categoría creada, incluyendo su ID como String
    except PyMongoError as e:
        # Manejar la excepción de MongoDB
        print(f"Error al insertar categoría: {e}")
        return None

def create_product(product: Product):
    new_product = product.dict()
    try:
        # Verificar si producto ya existe
        if products_collection.find_one({"name": new_product["name"]}):
            return None  # O manejar como prefieras
        

        result = products_collection.insert_one(new_product)
        new_product_id = result.inserted_id
        new_product["_id"] = str(new_product_id)  # Convierte ObjectId a String
        return new_product  # Devuelve producto creada, incluyendo su ID como String
    except PyMongoError as e:
        # Manejar la excepción de MongoDB
        print(f"Error al insertar categoría: {e}")
        return None

# UPDATES
def update_product(product_id: str, updated_product: Product):
    updated_data = updated_product.dict(
        exclude_unset=True)  # Excluye campos vacíos
    result = products_collection.update_one(
        {"_id": ObjectId(product_id)}, {"$set": updated_data})
    if result.modified_count > 0:
        return {"message": "Product updated"}
    elif result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        raise HTTPException(status_code=422, detail="Update operation failed")

def update_category(category_id: str, updated_category: Category):
    updated_data = updated_category.dict(exclude_unset=True)
    result = categories_collection.update_one(
        {"_id": ObjectId(category_id)}, {"$set": updated_data})
    if result.modified_count > 0:
        return {"message": "Category updated"}
    elif result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    else:
        raise HTTPException(status_code=422, detail="Update operation failed")

# DELETES
def delete_category(category_id: str):
    if not is_valid_object_id(category_id):
        raise HTTPException(status_code=400, detail="Invalid category ID")

    result = categories_collection.delete_one({"_id": ObjectId(category_id)})
    if result.deleted_count > 0:
        return {"message": "Category deleted"}
    elif result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    else:
        raise HTTPException(
            status_code=422, detail="Deletion operation failed")

def delete_product(product_id: str):
    if not is_valid_object_id(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")

    result = products_collection.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count > 0:
        return {"message": "Product deleted"}
    elif result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        raise HTTPException(
            status_code=422, detail="Deletion operation failed")
