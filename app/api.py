from fastapi import APIRouter, HTTPException, Path, Query, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import List
from models import Product, Category, UserCreate, UserResponse, LoginUser, UserUpdate
import database
from utils import is_valid_object_id, verify_password
from pydantic import EmailStr
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv



router = APIRouter()

""" -------------------- LOGIN ------------------------- """
# Obtener secret_key
load_dotenv("config.env")
secret_key = os.getenv("JWT_SECRET_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Instancia del esquema OAuth2

# Función para obtener el token JWT y verificarlo
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Verificar el token aquí decodificándolo
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        # Obtener el ID del usuario desde el token
        user_id: str = payload.get("sub")
        # Aquí deberías implementar la lógica para obtener el usuario desde la base de datos
        user = database.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")
        return user  # Retorna todo el objeto de usuario en lugar del ID solamente
    except JWTError:
        raise HTTPException(status_code=401, detail="No se pudo validar las credenciales")

# Función de dependencia para verificar el rol del usuario
async def check_user_role(current_user: dict = Depends(get_current_user)):
    # Verificar que el usuario tenga el rol necesario para consultar usuarios por email
    allowed_roles = ['super-admin', 'admin', 'user']
    if not any(role in allowed_roles for role in current_user["roles"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado. Se requiere rol de 'super-admin', 'admin' o 'user'")
    return current_user

# Login     
@router.post(
    "/login",
    summary="Iniciar sesión de usuario",
    description="Endpoint para permitir a los usuarios iniciar sesión. Proporciona las credenciales de usuario en el cuerpo de la solicitud. "
                "Si las credenciales son válidas, devuelve un mensaje de inicio de sesión exitoso."
)
async def login(user_data: LoginUser):
    user = database.get_user_by_email(user_data.email)
    
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    
    # Verificar contraseña
    if not verify_password(user_data.password, user['password']):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    # Payload del token JWT con información del usuario (puede incluir el ID, nombre, etc.)
    token_payload = {
        'sub': user['id'],  # ID del usuario
        'name': user['username'],  # Nombre del usuario
        'exp': datetime.utcnow() + timedelta(minutes=30)  # Tiempo de expiración del token (30 minutos, por ejemplo)
    }
    
    
    # Generar el token JWT
    token = jwt.encode(token_payload, secret_key, algorithm='HS256')
    
    # Devolver el token en la respuesta
    return {"message": "Inicio de sesión exitoso", "access_token": token, "token_type": "bearer"}  

""" ----------------- CATEGORIAS Y PRODUCTOS ---------------------- """
# Consultar las categorías y sus productos
@router.get("/categories/", response_model=List[Category],
            summary="Obtener todas las categorías",
            description="Este endpoint devuelve una lista de todas las categorías disponibles.")
def read_categories():
    categories = database.get_categories()
    return categories


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
                "Ejemplo de solicitud con paginacón: ```products/?page=1&page_size=10```"
)
def read_products(page: int = Query(1, description="Número de página", ge=1), 
                  page_size: int = Query(10, description="Tamaño de página", ge=1, le=100)):
    return database.get_paginated_products(page, page_size)

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
def create_category(category: Category, current_user: dict = Depends(check_user_role)):
    if "super-admin" not in current_user["roles"] and "admin" not in current_user["roles"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado. Se requiere rol de 'super-admin' o 'admin'")
    
    # Realiza la validación de los campos requeridos
    if not category.name:
        raise HTTPException(status_code=400, detail="Name required")
    if not category.image:
        raise HTTPException(status_code=400, detail="Image required")
    
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
                "Los detalles del producto, como nombre, descripción, categoría, etiquetas,precio, e imagen "
                "deben ser proporcionados en el cuerpo de la solicitud. "
                "Después de crear el producto con éxito, se devuelve un mensaje confirmando la creación."
)
def create_product(product: Product, current_user: dict = Depends(check_user_role)):
    # Verificar si el usuario tiene el rol necesario para crear productos
    if "super-admin" not in current_user["roles"] and "admin" not in current_user["roles"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado. Se requiere rol de 'super-admin' o 'admin'")
    
    # Realiza la validación de los campos requeridos
    if not product.name or not product.description or not product.category_id or not product.tags or not product.price or not product.image:
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
def update_category(category_id: str, updated_fields: dict, current_user: dict = Depends(check_user_role)):
    # Verificar que el usuario tenga el rol necesario para actualizar categorías
    if "super-admin" not in current_user["roles"] and "admin" not in current_user["roles"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado. Se requiere rol de 'super-admin' o 'admin'")
    
    if not is_valid_object_id(category_id):
        raise HTTPException(status_code=400, detail="Invalid category ID")
    
    # Verificar que se proporcionaron campos para actualizar
    if not updated_fields:
        raise HTTPException(status_code=400, detail="No fields to update provided")
    
    updated = database.update_category(category_id, updated_fields)
    if updated:
        return {"message": "Category updated"}
    raise HTTPException(status_code=404, detail="Category not found")

# Actualizar un producto
@router.put(
    "/products/{product_id}",
    summary="Actualizar un producto",
    description="Este endpoint permite realizar actualizaciones en un producto existente en la base de datos, "
                "identificado por su ID. El ID del producto debe ser proporcionado en la URL. Puedes enviar un "
                "objeto JSON en el cuerpo de la solicitud con los campos que deseas actualizar. Los campos no "
                "proporcionados en la solicitud permanecerán sin cambios. Si la actualización es exitosa, retorna "
                "un mensaje de confirmación. En caso de que el ID no sea válido o el producto no se encuentre, "
                "se retornará un error.\n\n"
                "Ejemplo de solicitud JSON para actualizar solo el nombre y el precio de un producto:\n"
                "```json\n"
                "{\n"
                "  \"name\": \"Nuevo Nombre\",\n"
                "  \"price\": 14.99\n"
                "}\n"
                "```\n"
                "Esto actualizará solo el nombre y el precio del producto sin afectar otros campos."
)
def update_product(product_id: str, updated_fields: dict, current_user: dict = Depends(check_user_role)):
    # Verificar que el usuario tenga el rol necesario para actualizar productos
    if "super-admin" not in current_user["roles"] and "admin" not in current_user["roles"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado. Se requiere rol de 'super-admin' o 'admin'")
    
    if not is_valid_object_id(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    
    # Verificar que se proporcionaron campos para actualizar
    if not updated_fields:
        raise HTTPException(status_code=400, detail="No fields to update provided")
    
    updated = database.update_product(product_id, updated_fields)
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
def delete_product(product_id: str, current_user: dict = Depends(check_user_role)):
    # Verificar que el usuario tenga el rol necesario para eliminar productos
    if "super-admin" not in current_user["roles"] and "admin" not in current_user["roles"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado. Se requiere rol de 'super-admin' o 'admin'")
    
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
def delete_category(category_id: str, current_user: dict = Depends(check_user_role)):
    # Verificar que el usuario tenga el rol necesario para eliminar categorias
    if "super-admin" not in current_user["roles"] and "admin" not in current_user["roles"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado. Se requiere rol de 'super-admin' o 'admin'")
    if not is_valid_object_id(category_id):
        raise HTTPException(status_code=400, detail="Invalid category ID")
    
    # Verificar si la categoría tiene productos asociados
    if database.category_has_products(category_id):
        raise HTTPException(status_code=422, detail="Category has associated products. Delete products first.")

    deleted = database.delete_category(category_id)
    if deleted.get("message") == "Category deleted":
        return deleted
    raise HTTPException(status_code=404, detail="Category not found")


""" -------------------- USUARIOS ------------------------- """
# Consultar usuario por id
@router.get(
    "/users/{user_id}", 
    response_model=UserResponse,
    summary="Consultar usuario por ID",
    description="Este endpoint permite obtener la información detallada de un usuario específico, "
                "identificada por su ID. Si el ID del usuario es válido y existe el usuario en la base de datos, "
                "retorna todos sus detalles. "
                "En caso de que el ID no sea válido o no exista, se retornará un error."
)
def read_user_by_id(user_id: str = Path(..., title="The ID of the user to get")):
    if not is_valid_object_id(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
        
    user = database.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Consultar usuario por email
@router.get(
    "/users/by_email/{user_email}", 
    response_model=UserResponse,
    dependencies=[Depends(check_user_role)],
    summary="Consultar usuario por email",
    description="Este endpoint permite obtener la información detallada de un usuario específico, "
                "identificada por su email. Si el email del usuario existe en la base de datos, "
                "retorna todos sus detalles. "
                "En caso de que el email no exista, se retornará un error."
)
def read_user_by_email(user_email: EmailStr):
    user = database.get_user_by_email(user_email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# Consultar usuarios por nombre
@router.get(
    "/users/by_names/{username}", 
    response_model=List[UserResponse],
    summary="Consultar usuarios por su nombre",
    dependencies=[Depends(check_user_role)],
    description="Este endpoint permite obtener la información detallada de usuarios con nombres similares"
                "Si el nombre del usuario existe en la base de datos, "
                "retorna todos sus detalles por usuario. "
)
def read_users_by_names(username: str):
    users= database.get_users(username)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return users

# Crear usuario
@router.post(
    "/users/",status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo usuario",
    description="Este endpoint permite crear un nuevo usuario en la base de datos. "
                "La información del usuario debe ser proporcionada en el cuerpo de la solicitud. "
                "Tras la creación exitosa, retorna un mensaje confirmando que el usuario ha sido creado."
)
def create_user(user: UserCreate):
    # Realiza la validación de los campos requeridos
    if not user.email:
        raise HTTPException(status_code=400, detail="Email required")
    if not user.password:
        raise HTTPException(status_code=400, detail="Password required")
    
    # Verificar si existe usuario
    if database.user_exists(user.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    try:
        created_user = database.create_user(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "User created", "user": created_user}

# Actualizar usuario
@router.put(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Actualizar información de usuario",
    description="Este endpoint permite actualizar la información de un usuario existente en la base de datos. "
                "Proporciona el ID del usuario en la URL y la información actualizada en el cuerpo de la solicitud. "
                "Si la actualización es exitosa, retorna la información actualizada del usuario."
)
def update_user_info(
    user_id: str,
    updated_info: UserUpdate,
    current_user: dict = Depends(check_user_role)
):
    """
    Actualiza la información de un usuario existente.

    - **user_id**: El ID del usuario a actualizar.
    - **updated_info**: La información actualizada del usuario (proporcionada en el cuerpo de la solicitud).
    """
    # Verificar que el usuario tenga el rol necesario para actualizar información de usuarios
    if "super-admin" not in current_user["roles"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado. Se requiere rol de 'super-admin'")
    
    if not is_valid_object_id(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    updated_user, response_status = database.update_user(user_id, updated_info)

    if response_status == status.HTTP_404_NOT_FOUND:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no existe.")

    elif response_status == status.HTTP_409_CONFLICT:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No se pudo actualizar el usuario, el correo electrónico ya está en uso.")

    elif response_status == status.HTTP_200_OK:
        return updated_user

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error desconocido")

# Eliminar usuario
@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Este endpoint permite eliminar un usuario existente en la base de datos proporcionando su ID.",
)
def delete_user_endpoint(user_id: str, current_user: dict = Depends(check_user_role)):
    """
    Elimina un usuario existente por su ID.

    - **user_id**: El ID del usuario a eliminar.
    """
    # Verificar que el usuario tenga el rol necesario para eliminar usuarios
    if "super-admin" not in current_user["roles"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado. Se requiere rol de 'super-admin'")
    
    if not is_valid_object_id(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    try:
        if database.delete_user(user_id):
            return None  # No content response on successful deletion
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró el usuario para eliminar")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

