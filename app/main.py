from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api import router as api_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

# Agregar la ruta para servir archivos estáticos, incluido el favicon
app.mount("/static", StaticFiles(directory="assets"), name="static")

# Incluir las rutas de tu API
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
