from contextlib import asynccontextmanager
from fastapi import FastAPI
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


@app.get("/")
def read_root():
<<<<<<< Updated upstream
    return {"mensagem": "Bem-vindo à API GUARA", "status": "online"}
=======
    return {"message": "Bem-vindo ao GUARA APP", "status": "online"}
>>>>>>> Stashed changes
