from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId, errors
from app.exceptions import NotFoundException, DatabaseException

class BaseRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def _validate_id(self, id: str):
        try:
            return ObjectId(id)
        except errors.InvalidId:
            raise NotFoundException("ID inválido")

    async def find_by_id(self, id: str):
        try:
            obj_id = await self._validate_id(id)
            document = await self.collection.find_one({"_id": obj_id})
            if not document:
                raise NotFoundException("Documento no encontrado")
            document["_id"] = str(document["_id"])
            return document
        except NotFoundException:
            raise  # Propaga la excepción directamente
        except Exception as e:
            raise DatabaseException(f"Error de base de datos: {str(e)}")

    async def update(self, id: str, update_data: dict):
        try:
            obj_id = await self._validate_id(id)
            result = await self.collection.update_one(
                {"_id": obj_id}, {"$set": update_data}
            )
            if result.matched_count == 0:
                raise NotFoundException("Documento a actualizar no encontrado")
            return await self.find_by_id(id)
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al actualizar: {str(e)}")

    async def delete(self, id: str):
        try:
            obj_id = await self._validate_id(id)
            result = await self.collection.delete_one({"_id": obj_id})
            if result.deleted_count == 0:
                raise NotFoundException("Documento a eliminar no encontrado")
            return True
        except NotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Error al eliminar: {str(e)}")