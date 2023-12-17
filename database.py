from pymongo import MongoClient
from models import Product, Category
from bson import ObjectId
import os

# Obtiene la cadena de conexión desde las variables de entorno
mongo_uri = os.getenv("MONGO_URI")

# Conexión a MongoDB
client = MongoClient(mongo_uri) 
#client = MongoClient('mongodb://localhost:27017/') 
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
    return products_collection.find_one({"_id": ObjectId(product_id)}, {"_id": 0})

def create_category(category: Category):
    new_category = category.dict()
    categories_collection.insert_one(new_category)

def create_product(product: Product):
    new_product = product.dict()
    products_collection.insert_one(new_product)

def delete_product(product_id: str):
    products_collection.delete_one({"_id": ObjectId(product_id)})

def update_product(product_id: str, updated_product: Product):
    products_collection.update_one({"_id": ObjectId(product_id)}, {"$set": updated_product.dict()})
