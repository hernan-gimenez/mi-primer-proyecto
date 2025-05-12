from fastapi import FastAPI, Depends, HTTPException, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Dict, Any
import os
from sqlalchemy.orm import Session

from src.domain.link import Link
from src.application.use_cases import LinkService
from src.application.ports import LinkRepository
from src.infrastructure.repositories.sqlite_link_repository import SQLiteLinkRepository
from src.infrastructure.database.database import get_db, init_db

# Modelo Pydantic para la entrada de enlaces
class LinkCreate(BaseModel):
    url: str

# Inicializar la base de datos
init_db()

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar rutas estáticas
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "../../../static")), name="static")

# Configurar templates
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "../../../templates"))

def get_link_service(db: Session = Depends(get_db)) -> LinkService:
    repository = SQLiteLinkRepository(db)
    return LinkService(repository)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return FileResponse(os.path.join(os.path.dirname(__file__), "../../../static/index.html"))

@app.post("/api/links/")
async def create_link(link_data: dict, service: LinkService = Depends(get_link_service)):
    print("Datos recibidos:", link_data)  # Debug log
    
    if not link_data or 'url' not in link_data or not link_data['url'].strip():
        raise HTTPException(
            status_code=422,
            detail={"error": "URL is required", "received_data": link_data}
        )
    
    try:
        url = link_data['url'].strip()
        print(f"Intentando guardar URL: {url}")  # Debug log
        link = await service.create_link(url)
        return {
            "id": link.id,
            "url": link.url,
            "created_at": link.created_at.isoformat() if link.created_at else None
        }
    except ValueError as e:
        print(f"Error de validación: {str(e)}")  # Debug log
        raise HTTPException(status_code=400, detail={"error": str(e)})
    except Exception as e:
        print(f"Error inesperado: {str(e)}")  # Debug log
        raise HTTPException(
            status_code=500,
            detail={"error": "Internal server error", "details": str(e)}
        )

@app.get("/api/links/")
async def list_links(service: LinkService = Depends(get_link_service)):
    try:
        links = await service.list_links()
        return [{"id": link.id, "url": link.url, "created_at": link.created_at} for link in links]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/links/{link_id}")
async def delete_link(link_id: int, service: LinkService = Depends(get_link_service)):
    try:
        success = await service.remove_link(link_id)
        if not success:
            raise HTTPException(status_code=404, detail="Link not found")
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
