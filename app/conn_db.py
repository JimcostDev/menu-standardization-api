from pymongo import MongoClient, TEXT
import os
from dotenv import load_dotenv
class Database:
    def __init__(self, mongo_uri: str):
        self.client = MongoClient(mongo_uri)
        self.db = self.client['api_menu_db']

        # Colecciones en la base de datos
        self.products_collection = self.db['products']
        self.categories_collection = self.db['categories']
        self.users_collection = self.db['users']

        # Crear índices de texto
        self.categories_collection.create_index([("name", TEXT)])
        self.products_collection.create_index([("name", TEXT)])
        self.users_collection.create_index([("email", TEXT)])

    def get_db(self):
        return self.db

    def close_connection(self):
        self.client.close()
        
# Función para obtener una instancia de la base de datos
def get_database_instance():
    # Obtener la cadena de conexión desde config.env
    load_dotenv("config.env")
    mongo_uri = os.getenv("MONGO_URI")

    # Instanciar la clase Database para manejar la conexión
    db = Database(mongo_uri)
    return db