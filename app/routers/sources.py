from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import DataSource
from app.dependencies import get_db

router = APIRouter(prefix="/sources", tags=["Источники данных"])

@router.get("/")
def get_sources(db: Session = Depends(get_db)):
    return db.query(DataSource).all()