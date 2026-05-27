"""
main.py — Punto de entrada principal de la aplicación FastAPI.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import engine, Base
from app.routers import personas

# Crear las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Personas",
    description="CRUD de Personas con FastAPI, Jinja2, HTML5 y SQLite",
    version="1.0.0"
)

# Servir archivos estáticos y plantillas desde la raíz del proyecto
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Incluir las rutas del CRUD
app.include_router(personas.router)


@app.get("/", response_class=HTMLResponse)
def read_index(request: Request):
    """Renderiza la interfaz frontend SPA del CRUD."""
    return templates.TemplateResponse(request=request, name="index.html")
