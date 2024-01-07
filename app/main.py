from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from api import router as api_router

app = FastAPI(
    title="Estandarización de Menús para Restaurantes",
    description="Esta API ofrece operaciones CRUD (Crear, Leer, Actualizar y Eliminar) para gestionar categorías, productos y usuarios, permitiendo a los restaurantes organizar y presentar sus menús de manera eficiente.",
    version="0.1.0"
)

# Configurar CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Reemplaza esto con el origen de tu aplicación web
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hola Mundo!"}

# Agregar la ruta para servir archivos estáticos, incluido el favicon
app.mount("/static", StaticFiles(directory="assets"), name="static")

# Incluir las rutas de tu API
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
