# API de Estandarización de Menús para Restaurantes

Este proyecto se centra en proporcionar una API robusta que facilite la estandarización de menús para restaurantes. Ofrece un conjunto completo de operaciones CRUD (Crear, Leer, Actualizar y Eliminar) diseñadas para la gestión ágil de categorías y productos, así como funcionalidades completas para la administración de usuarios. Esto permite a los restaurantes organizar y presentar sus menús de manera eficiente y flexible, mientras gestionan fácilmente la información de sus clientes y empleados.

## Características

- **Manejo de Categorías y Productos**: Operaciones para administrar categorías y productos, incluyendo la creación, actualización, eliminación y visualización de detalles como nombre, descripción, etiquetas (vegano, gluten free, picante), precio, entre otros.
- **Flexibilidad de Personalización:** Facilidad para añadir etiquetas personalizadas a los productos para una mejor clasificación (etiquetas especiales, alérgenos, etc.).
- **Autenticación de Usuarios:** Implementación de endpoints para la gestión de usuarios, incluyendo registro, inicio de sesión, consulta, actualización y eliminación de usuarios.

## Tecnologías Utilizadas

[![FastAPI](https://img.shields.io/badge/FastAPI-00599C?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=101010)](https://fastapi.tiangolo.com/)

**FastAPI:** Un framework web moderno y de alto rendimiento para construir APIs rápidas en Python.

[![Python](https://img.shields.io/badge/Python-1f425f?style=for-the-badge&logo=python&logoColor=white&labelColor=101010)]()

**Python:** El lenguaje de programación versátil, potente y fácil de aprender que permite una gran flexibilidad en el desarrollo de aplicaciones.

[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white&labelColor=101010)]()

**MongoDB:** Una base de datos NoSQL versátil y escalable utilizada para almacenar y gestionar datos de manera eficiente y flexible.

[![bcrypt](https://img.shields.io/badge/bcrypt-00457C?style=for-the-badge&logoColor=white&labelColor=101010)]()

**bcrypt:** Una herramienta de hashing que garantiza el almacenamiento seguro de contraseñas mediante algoritmos de encriptación sólidos.

[![pydantic](https://img.shields.io/badge/pydantic-DA11FF?style=for-the-badge&logo=Python&logoColor=white&labelColor=101010)](https://pydantic-docs.helpmanual.io/)

**pydantic:** Una poderosa biblioteca Python para validar y manipular datos con facilidad, incluyendo soporte para análisis y generación de archivos YAML.




## Instalación

1. Clona este repositorio ejecutando el siguiente comando:
    ```
    git clone https://github.com/JimcostDev/menu-standardization-api.git
    ```

2. Crea y activa tu entorno virtual:
    - Crea un entorno virtual:
        ```
        python -m venv venv
        ```
    - Activa el entorno virtual:
        - En Windows:
            ```
            venv\Scripts\activate
            ```
        - En macOS y Linux:
            ```
            source venv/bin/activate
            ```

3. Instala las dependencias requeridas:
    ```
    pip install -r requirements.txt
    ```

4. Crea un archivo llamado `config.env` dentro de la carpeta `app`. Este archivo se utiliza para cargar las variables de entorno necesarias para la aplicación, como la `JWT_SECRET_KEY` y `MONGO_URI`. El archivo `config.env` debe contener:
    ```plaintext
    MONGO_URI=your_secret_key_here
    JWT_SECRET_KEY=your_secret_key_here
    ```
    
5. Configura la base de datos MongoDB, se llama `api_menu_db` con las colecciones `categories`, `products`, y `users` para el correcto funcionamiento de la aplicación.

6. Dirígete al directorio de la aplicación:
    ```
    cd app
    ```

7. Ejecuta la aplicación con el siguiente comando:
    ```
    uvicorn main:app --reload
    ```
Esta acción iniciará el servidor de desarrollo y podrás acceder a la aplicación desde tu navegador en `http://localhost:8000`.


## Uso

1. Inicia la aplicación. (paso 7)
2. Accede a `http://localhost:8000` para interactuar con la API.
3. Utiliza herramientas como Postman o Insomnia para probar los endpoints.

### Endpoints

#### Autenticación
- `POST /login`
  
#### Categorías
- `GET /categories/`
- `GET /categories/{category_id}`
- `POST /categories/`
- `PUT /categories/{category_id}`
- `DELETE /categories/{category_id}`

#### Productos
- `GET /products/`
- `GET /products/{product_id}`
- `GET /categories/{category_id}/products/`
- `POST /products/`
- `PUT /products/{product_id}`
- `DELETE /products/{product_id}`

#### Usuarios
- `GET /users/{user_id}`
- `GET /users/by_email/{user_email}`
- `GET /users/by_names/{username}`
- `POST /users/`
- `PUT /users/{user_id}`
- `DELETE /users/{user_id}`


## Contribución

¡Gracias por considerar contribuir a este proyecto! Si deseas agregar nuevas características, solucionar problemas existentes o mejorar la aplicación de alguna manera, aquí hay algunos pasos para comenzar:

1. Haz un fork del repositorio a través del botón de "Fork" en la parte superior derecha de esta página.
   
2. Clona tu repositorio forkeado:
    ```bash
    git clone https://github.com/TU_USUARIO/nombre-del-repositorio.git
    ```

3. Crea una nueva rama para trabajar en tu característica:
    ```bash
    git checkout -b feature/nueva-caracteristica
    ```

4. Realiza los cambios necesarios y añade tus contribuciones:
    ```bash
    git add .
    git commit -m 'Agrega nueva característica'
    ```

5. Sube tus cambios a tu repositorio en GitHub:
    ```bash
    git push origin feature/nueva-caracteristica
    ```

6. Abre un Pull Request desde tu rama a la rama principal de este repositorio.
   
Una vez abierto, tu Pull Request será revisado y, si todo está correcto, será fusionado. ¡Gracias por tu contribución!

