from app.core.database import mongodb
from app.repositories.base_repository import BaseRepository

class ProductRepository(BaseRepository):
    def __init__(self):
        super().__init__(None) 
        
    def initialize(self):
        """Inicializa la colección cuando la conexión a MongoDB está lista"""
        if self.collection is None:  
            self.collection = mongodb.get_collection("products")
        
    async def get_all(self):
        """Obtiene todos los productos."""
        self.initialize()
        return await self.find_all()

    async def get_by_id(self, id: str):
        """Obtiene un producto por su ID."""
        self.initialize()
        return await self.find_by_id(id)

    async def create(self, product: dict):
        """Crea un nuevo producto."""
        self.initialize()
        return await super().create(product) 

    async def update(self, id: str, update_data: dict):
        """Actualiza un producto existente."""
        self.initialize()
        return await super().update(id, update_data)  

    async def delete(self, id: str):
        """Elimina un producto por su ID."""
        self.initialize()
        return await super().delete(id)