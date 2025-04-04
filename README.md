# API para Menús de Restaurantes

Este proyecto es una API REST diseñada para la gestión integral de productos, construida con la potencia y flexibilidad de FastAPI y la escalabilidad de MongoDB. Su objetivo principal es servir como una herramienta de aprendizaje y demostración de las capacidades de estas tecnologías en un entorno práctico.

## Instalación
> [!NOTE]
> Asegúrate de tener Git instalado antes de clonar.

1. **Clonar el repositorio**  
   Ejecuta el siguiente comando:
   ```bash
   git clone https://github.com/JimcostDev/menu-standardization-api.git
   ```
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
> [!IMPORTANT]
> Dentro de la carpeta `app/core`, crea un archivo llamado `config.env` para cargar las variables necesarias, como `MONGODB_URI_DEV_LAB_TEST` y `MONGODB_NAME`. El archivo debe tener el siguiente formato:

4. **Configurar variables de entorno**
   ```plaintext
   MONGODB_URI_DEV_LAB_TEST=your_secret_key_here
   MONGODB_NAME=your_secret_key_here
   ```


5. **Configurar la base de datos**  
   Configura la base de datos MongoDB con el nombre `api_menu_db` y asegúrate de que existan las colección: `products` para el correcto funcionamiento de la aplicación.

---


