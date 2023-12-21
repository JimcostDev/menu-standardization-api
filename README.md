# Estandarización de Menús para Restaurantes

Este proyecto se enfoca en desarrollar una API que permita la estandarización de menús para restaurantes. La API ofrece operaciones CRUD (Crear, Leer, Actualizar y Eliminar) para gestionar categorías y productos, permitiendo a los restaurantes organizar y presentar sus menús de manera eficiente.

## Características

- **Manejo de Categorías y Productos**: Operaciones para administrar categorías y productos, incluyendo la creación, actualización, eliminación y visualización de detalles como nombre, descripción, etiquetas (vegano, gluten free, picante), precio, entre otros.

- **Flexibilidad de Personalización:** Facilidad para añadir etiquetas personalizadas a los productos para una mejor clasificación (etiquetas especiales, alérgenos, etc.).

## Tecnologías Utilizadas

- Python
- FastAPI
- Pydantic
- MongoDB

## Instalación

1. Clona este repositorio: `git clone`
2. Crea tu entorno virtual `python -m venv venv` y activalo :  `source venv/Scripts/activate`
3. Instala las dependencias usando `pip install -r requirements.txt`.
4. Configura la base de datos MongoDB (colecciones: categories y products)
5. `cd app`
6. Ejecuta la aplicación usando `uvicorn main:app --reload`.

## Uso

1. Inicia la aplicación.
2. Accede a `http://localhost:8000` para interactuar con la API.
3. Utiliza herramientas como Postman para probar los endpoints.

## Endpoints

- `/categories`: Obtener todas las categorías.
- `/categories/{category_id}/products`: Obtener productos por categoría.
- `/products`: Obtener todos los productos.
- `/products/{product_id}`: Obtener producto por ID.
- `/categories/{category_id}`: Obtener categoria por ID.
- `/categories/`: Crear una nueva categoría.
- `/products/`: Crear un nuevo producto.
- `/products/{product_id}`: Eliminar o actualizar un producto por ID.
- `/categories/{category_id}`: Eliminar o actualizar una categoria por ID.

## Contribución

1. Haz un fork del repositorio.
2. Crea una rama (`git checkout -b feature/nueva-caracteristica`).
3. Haz commit de tus cambios (`git commit -am 'Agrega nueva característica'`).
4. Haz push de la rama (`git push origin feature/nueva-caracteristica`).
5. Abre un Pull Request.

