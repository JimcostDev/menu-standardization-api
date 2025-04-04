from app.models.products import ProductCreate, ProductResponse, ProductUpdate
from app.repositories.product_repository import ProductRepository

class ProductService:
    repository = ProductRepository()
    
    @classmethod
    async def get_all_products(cls) -> list[ProductResponse]:
        """Obtiene todos los productos."""
        products = await cls.repository.get_all()
        return [ProductResponse(**product) for product in products] if products else []
    
    @classmethod
    async def get_product_by_id(cls, product_id: str) -> ProductResponse:
        """Obtiene un producto por su ID."""
        product = await cls.repository.get_by_id(product_id)
        return ProductResponse(**product)
    
    @classmethod
    async def create_product(cls, product: ProductCreate) -> ProductResponse:
        """Crea un nuevo producto."""
        # Convertir a diccionario y luego a JSON y de vuelta a diccionario para asegurar serialización
        product_dict = product.model_dump(mode='json')
        
        # Conversión explícita de HttpUrl a string si es necesario
        if 'category' in product_dict and 'image' in product_dict['category']:
            product_dict['category']['image'] = str(product_dict['category']['image'])
        
        if 'image' in product_dict:
            product_dict['image'] = str(product_dict['image'])
            
        created_product = await cls.repository.create(product_dict)
        return ProductResponse(**created_product)
    
    @classmethod
    async def update_product(cls, product_id: str, product: ProductUpdate) -> ProductResponse:
        """Actualiza un producto existente."""
        # Convertir a formato JSON para garantizar que MongoDB pueda manejarlo
        product_dict = product.model_dump(exclude_unset=True, mode='json')
        
        # Conversión explícita de HttpUrl a string si es necesario
        if 'category' in product_dict and 'image' in product_dict['category']:
            product_dict['category']['image'] = str(product_dict['category']['image'])
        
        if 'image' in product_dict:
            product_dict['image'] = str(product_dict['image'])
            
        updated_product = await cls.repository.update(product_id, product_dict)
        return ProductResponse(**updated_product)
    
    @classmethod
    async def delete_product(cls, product_id: str) -> bool:
        """Elimina un producto por su ID."""
        return await cls.repository.delete(product_id)