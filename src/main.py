"from fastapi import FastAPI
from sqlmodel import create_engine, Session
from src.models.base import Base
from src.models.user import User
from src.models.article import Article

# Create FastAPI app
app = FastAPI(title=\"GUARA\", version=\"1.0.0\")

# Database setup
DATABASE_URL = \"postgresql://user:password@localhost/guara_db\"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

# Include routers
from src.api.main_router import router as main_router
app.include_router(main_router, prefix=\"/api\")
