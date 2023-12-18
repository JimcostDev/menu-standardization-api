from fastapi import APIRouter, HTTPException, Path
from typing import List
from app.models import Product, Category
from app import database
from app.utils import is_valid_object_id

router = APIRouter()

# Consultar las categorías y sus productos
@router.get("/categories/", response_model=List[Category])
def read_categories():
    return database.get_categories()


@router.get("/categories/{category_name}/products/", response_model=List[Product])
def read_category_products(category_name: str):
    return database.get_category_products(category_name)

# Consultar los productos
@router.get("/products/", response_model=List[Product])
def read_products():
    return database.get_products()

# Consultar por id de producto
@router.get("/products/{product_id}", response_model=Product)
def read_product(product_id: str = Path(..., title="The ID of the product to get")):
    if not is_valid_object_id(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")

    product = database.get_product_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product

# Consultar por id de categoría
@router.get("/categories/{category_id}", response_model=Category)
def read_category(category_id: str = Path(..., title="The ID of the category to get")):
    if not is_valid_object_id(category_id):
        raise HTTPException(status_code=400, detail="Invalid category ID")

    category = database.get_category_by_id(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return category


# Crear una categoría
@router.post("/categories/")
def create_category(category: Category):
    database.create_category(category)
    return {"message": "Category created"}

# Crear un producto
@router.post("/products/")
def create_product(product: Product):
    database.create_product(product)
    return {"message": "Product created"}

# Eliminar un producto
@router.delete("/products/{product_id}")
def delete_product(product_id: str):
    if not is_valid_object_id(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")

    deleted = database.delete_product(product_id)
    if deleted.get("message") == "Product deleted":
        return deleted
    raise HTTPException(status_code=404, detail="Product not found")

# Eliminar una categoría
@router.delete("/categories/{category_id}")
def delete_category(category_id: str):
    if not is_valid_object_id(category_id):
        raise HTTPException(status_code=400, detail="Invalid category ID")

    deleted = database.delete_category(category_id)
    if deleted.get("message") == "Category deleted":
        return deleted
    raise HTTPException(status_code=404, detail="Category not found")


# Actualizar una categoría
@router.put("/categories/{category_id}")
def update_category(category_id: str, category: Category):
    updated = database.update_category(category_id, category)
    if updated:
        return {"message": "Category updated"}
    raise HTTPException(status_code=404, detail="Category not found")

# Actualizar un producto
@router.put("/products/{product_id}")
def update_product(product_id: str, product: Product):
    updated = database.update_product(product_id, product)
    if updated:
        return {"message": "Product updated"}
    raise HTTPException(status_code=404, detail="Product not found")
