# [!TIP] API para Menús de Restaurantes

Este es un proyecto de aprendizaje y proporciona una API sencilla para la gestión de productos. Implementa operaciones CRUD (Crear, Leer, Actualizar y Eliminar) para la administración de productos.

---

## Tecnologías Utilizadas

- [!NOTE] **FastAPI:** Framework web moderno y de alto rendimiento para construir APIs rápidas en Python.
- [!NOTE] **Python:** Lenguaje de programación versátil, potente y fácil de aprender, que ofrece gran flexibilidad en el desarrollo de aplicaciones.
- [!NOTE] **MongoDB:** Base de datos NoSQL versátil y escalable, utilizada para almacenar y gestionar datos de manera eficiente.

---

## Instalación

1. **Clonar el repositorio**  
   Ejecuta el siguiente comando:
   ```bash
   git clone https://github.com/JimcostDev/menu-standardization-api.git
   ```
   [!TIP] **Consejo:** Asegúrate de tener Git instalado antes de clonar.

2. **Crear y activar el entorno virtual**  
   - Crea el entorno virtual:
     ```bash
     python -m venv venv
     ```
   - Activa el entorno virtual:
     - En **Windows**:
       ```bash
       venv\Scripts\activate
       ```
     - En **macOS y Linux**:
       ```bash
       source venv/bin/activate
       ```

3. **Instalar dependencias**  
   Ejecuta:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**  
   Dentro de la carpeta `app/core`, crea un archivo llamado `config.env` para cargar las variables necesarias, como `MONGODB_URI_DEV_LAB_TEST` y `MONGODB_NAME`. El archivo debe tener el siguiente formato:
   ```plaintext
   MONGODB_URI_DEV_LAB_TEST=your_secret_key_here
   MONGODB_NAME=your_secret_key_here
   ```
   [!TIP] **Recomendación:** No olvides reemplazar `your_secret_key_here` por tus claves reales.

5. **Configurar la base de datos**  
   Configura la base de datos MongoDB con el nombre `api_menu_db` y asegúrate de que existan las colecciones: `products` para el correcto funcionamiento de la aplicación.

---

[!NOTE] **Importante:** Sigue cada paso cuidadosamente para evitar errores en la configuración inicial de la API. ¡Disfruta del aprendizaje y la experiencia de desarrollo!

