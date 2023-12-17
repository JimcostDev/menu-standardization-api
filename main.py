from fastapi import FastAPI
from typing import List
from models import Product, Category
import database

app = FastAPI()

# Consultar las categorías y sus productos
@app.get("/categories/", response_model=List[Category])
def read_categories():
    return database.get_categories()

@app.get("/categories/{category_name}/products/", response_model=List[Product])
def read_category_products(category_name: str):
    return database.get_category_products(category_name)

# Consultar los productos
@app.get("/products/", response_model=List[Product])
def read_products():
    return database.get_products()

# Consultar por id
@app.get("/products/{product_id}", response_model=Product)
def read_product(product_id: str):
    return database.get_product_by_id(product_id)

# Crear una categoría
@app.post("/categories/")
def create_category(category: Category):
    database.create_category(category)
    return {"message": "Category created"}

# Crear un producto
@app.post("/products/")
def create_product(product: Product):
    database.create_product(product)
    return {"message": "Product created"}

# Eliminar un producto
@app.delete("/products/{product_id}")
def delete_product(product_id: str):
    database.delete_product(product_id)
    return {"message": "Product deleted"}

# Actualizar un producto
@app.put("/products/{product_id}")
def update_product(product_id: str, product: Product):
    database.update_product(product_id, product)
    return {"message": "Product updated"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
