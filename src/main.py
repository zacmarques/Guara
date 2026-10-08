from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from src.api.main_router import main_router
from src.api.deps import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="GUARA",
    description="Gerenciador Unificado de Atualização de Registros Acadêmicos",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(main_router, prefix="/api")


@app.get("/", response_class=HTMLResponse)
def read_root():
    template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>GUARA - Gerenciador Unificado de Registros Acadêmicos</h1>")
