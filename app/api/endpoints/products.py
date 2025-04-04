from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.products import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import ProductService
from app.exceptions import NotFoundException

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
async def list_products():
    """Endpoint para listar todos los productos."""
    return await ProductService.get_all_products()

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    """Endpoint para obtener un producto por su ID."""
    try:
        return await ProductService.get_product_by_id(product_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    """Endpoint para crear un nuevo producto."""
    return await ProductService.create_product(product)

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, product: ProductUpdate):
    """Endpoint para actualizar un producto existente."""
    try:
        return await ProductService.update_product(product_id, product)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: str):
    """Endpoint para eliminar un producto por su ID."""
    try:
        await ProductService.delete_product(product_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
