from pymongo import MongoClient
from app.models import Product, Category
from bson import ObjectId
from app.utils import is_valid_object_id
from fastapi import HTTPException
import os

# Obtiene la cadena de conexión desde las variables de entorno
mongo_uri = os.getenv("MONGO_URI")

# Conexión a MongoDB
# client = MongoClient(mongo_uri)
client = MongoClient('mongodb://localhost:27017/')
db = client['api_menu_db']

# Colecciones en la base de datos
products_collection = db['products']
categories_collection = db['categories']

# Operaciones en la base de datos


def get_categories() -> list:
    return list(categories_collection.find({}, {"_id": 0}))


def get_category_products(category_name: str) -> list:
    return list(products_collection.find({"category": category_name}, {"_id": 0}))


def get_products() -> list:
    return list(products_collection.find({}, {"_id": 0}))


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


def create_category(category: Category):
    new_category = category.dict()
    categories_collection.insert_one(new_category)


def create_product(product: Product):
    new_product = product.dict()
    products_collection.insert_one(new_product)


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
