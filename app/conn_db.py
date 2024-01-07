from pymongo import MongoClient, TEXT

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