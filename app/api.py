from fastapi import APIRouter, HTTPException, Path
from typing import List
from models import Product, Category
import database
from utils import is_valid_object_id

router = APIRouter()

# Consultar las categorías y sus productos
@router.get("/categories/", response_model=List[Category],
            summary="Obtener todas las categorías",
            description="Este endpoint devuelve una lista de todas las categorías disponibles.")
def read_categories():
    return database.get_categories()


@router.get("/categories/{category_id}/products/", response_model=List[Product],
            summary="Obtener productos por categoría",
            description="Devuelve todos los productos pertenecientes a una categoría específica. "
                        "La categoría se especifica por su ID.")
def read_category_products(category_id: str):
    return database.get_category_products(category_id)

# Consultar los productos
@router.get(
    "/products/", 
    response_model=List[Product],
    summary="Obtener todos los productos",
    description="Este endpoint devuelve una lista de todos los productos disponibles en la base de datos. "
                "Cada producto incluye detalles como nombre, descripción, categoría, etiquetas y precio. "
                "Es útil para obtener una vista general de todos los productos ofrecidos."
)
def read_products():
    return database.get_products()

# Consultar por id de producto
@router.get(
    "/products/{product_id}",
    response_model=Product,
    summary="Consultar producto por ID",
    description="Este endpoint permite obtener la información detallada de un producto específico, "
                "identificado por su ID. Si el ID del producto es válido y el producto existe en la base de datos, "
                "retorna todos los detalles del producto, incluyendo nombre, descripción, categoría, etiquetas y precio. "
                "En caso de que el ID no sea válido o el producto no exista, se retornará un error."
)
def read_product(product_id: str = Path(..., title="The ID of the product to get")):
    if not is_valid_object_id(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")

    product = database.get_product_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Consultar por id de categoría
@router.get(
    "/categories/{category_id}", 
    response_model=Category,
    summary="Consultar categoría por ID",
    description="Este endpoint permite obtener la información detallada de una categoría específica, "
                "identificada por su ID. Si el ID de la categoría es válido y la categoría existe en la base de datos, "
                "retorna todos los detalles de la categoría, como su nombre. "
                "En caso de que el ID no sea válido o la categoría no exista, se retornará un error."
)
def read_category(category_id: str = Path(..., title="The ID of the category to get")):
    if not is_valid_object_id(category_id):
        raise HTTPException(status_code=400, detail="Invalid category ID")

    category = database.get_category_by_id(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


# Crear una categoría
@router.post(
    "/categories/",
    summary="Crear una nueva categoría",
    description="Este endpoint permite crear una nueva categoría en la base de datos. "
                "Se debe proporcionar la información de la categoría en el cuerpo de la solicitud. "
                "Tras la creación exitosa, retorna un mensaje confirmando que la categoría ha sido creada."
)
def create_category(category: Category):
    # Realiza la validación de los campos requeridos
    if not category.name:
        raise HTTPException(status_code=400, detail="Name required")
    
    # Validación adicional, como verificar la unicidad del nombre de categoría
    if database.category_exists(category.name):
        raise HTTPException(status_code=400, detail="Category already exists")

    # Crear categoría y manejar posibles errores
    try:
        created_category = database.create_category(category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Category created", "category": created_category}

# Crear un producto
@router.post(
    "/products/",
    summary="Crear un nuevo producto",
    description="Este endpoint permite crear un nuevo producto en la base de datos. "
                "Los detalles del producto, como nombre, descripción, categoría, etiquetas y precio, "
                "deben ser proporcionados en el cuerpo de la solicitud. "
                "Después de crear el producto con éxito, se devuelve un mensaje confirmando la creación."
)
def create_product(product: Product):
    # Realiza la validación de los campos requeridos
    if not product.name or not product.description or not product.category_id or not product.tags or not product.price:
        raise HTTPException(status_code=400, detail="All fields are required")
    
    # Validación adicional, como verificar la unicidad del nombre de categoría
    if database.product_exists(product.name):
        raise HTTPException(status_code=400, detail="Product already exists")

    # Crear producto y manejar posibles errores
    try:
        created_product = database.create_product(product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Product created", "product": created_product}


# Actualizar una categoría
@router.put(
    "/categories/{category_id}",
    summary="Actualizar una categoría",
    description="Este endpoint actualiza los detalles de una categoría existente en la base de datos, "
                "identificada por su ID. El ID de la categoría debe ser proporcionado en la URL y los nuevos "
                "detalles de la categoría en el cuerpo de la solicitud. Si la actualización es exitosa, retorna "
                "un mensaje de confirmación. En caso de que el ID no sea válido o la categoría no se encuentre, "
                "se retornará un error."
)
def update_category(category_id: str, category: Category):
    if not is_valid_object_id(category_id):
        raise HTTPException(status_code=400, detail="Invalid category ID")
    
    # Realiza la validación de los campos requeridos
    if not category.name:
        raise HTTPException(status_code=400, detail="Name required")
    
    updated = database.update_category(category_id, category)
    if updated:
        return {"message": "Category updated"}
    raise HTTPException(status_code=404, detail="Category not found")

# Actualizar un producto
@router.put(
    "/products/{product_id}",
    summary="Actualizar un producto",
    description="Este endpoint actualiza los detalles de un producto existente en la base de datos, "
                "identificado por su ID. El ID del producto debe ser proporcionado en la URL y los nuevos "
                "detalles del producto en el cuerpo de la solicitud. Si la actualización es exitosa, retorna "
                "un mensaje de confirmación. En caso de que el ID no sea válido o el producto no se encuentre, "
                "se retornará un error."
)
def update_product(product_id: str, product: Product):
    if not is_valid_object_id(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    
    # Realiza la validación de los campos requeridos
    if not product.name or not product.description or not product.category_id or not product.tags or not product.price:
        raise HTTPException(status_code=400, detail="All fields are required")
    
    updated = database.update_product(product_id, product)
    if updated:
        return {"message": "Product updated"}
    raise HTTPException(status_code=404, detail="Product not found")

# Eliminar un producto
@router.delete(
    "/products/{product_id}",
    summary="Eliminar un producto",
    description="Este endpoint elimina un producto específico de la base de datos, identificado por su ID. "
                "El ID del producto debe ser proporcionado en la URL. Si el producto con el ID especificado existe, "
                "será eliminado y se retornará un mensaje de confirmación. "
                "Si el ID no es válido o el producto no se encuentra, se retornará un error."
)
def delete_product(product_id: str):
    if not is_valid_object_id(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")

    deleted = database.delete_product(product_id)
    if deleted.get("message") == "Product deleted":
        return deleted
    raise HTTPException(status_code=404, detail="Product not found")

# Eliminar una categoría
@router.delete(
    "/categories/{category_id}",
    summary="Eliminar una categoría",
    description="Este endpoint elimina una categoría específica de la base de datos, identificada por su ID. "
                "El ID de la categoría debe ser proporcionado en la URL. Si la categoría con el ID especificado existe, "
                "será eliminada y se retornará un mensaje de confirmación. "
                "Si el ID no es válido o la categoría no se encuentra, se retornará un error."
)
def delete_category(category_id: str):
    if not is_valid_object_id(category_id):
        raise HTTPException(status_code=400, detail="Invalid category ID")
    
    # Verificar si la categoría tiene productos asociados
    if database.category_has_products(category_id):
        raise HTTPException(status_code=422, detail="Category has associated products. Delete products first.")

    deleted = database.delete_category(category_id)
    if deleted.get("message") == "Category deleted":
        return deleted
    raise HTTPException(status_code=404, detail="Category not found")
