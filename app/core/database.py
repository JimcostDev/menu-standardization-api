from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class MongoDB:
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db = None
    
    async def connect(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URI_DEV_LAB_TEST)
        self.db = self.client[settings.MONGODB_NAME]
        await self.client.admin.command('ping')
        print("Conexión a MongoDB exitosa.")
    
    async def disconnect(self):
        if self.client:
            self.client.close()
            print("Conexión a MongoDB cerrada.")
    
    def get_collection(self, collection_name: str):
        """Obtiene una colección de forma segura"""
        if self.db is None:  
            raise RuntimeError("Base de datos no conectada. Llama a connect() primero.")
        return self.db[collection_name]

mongodb = MongoDB()