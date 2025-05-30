from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models import Industry, DataSource  # Убедись, что такие модели есть

router = APIRouter(prefix="/dictionaries", tags=["Справочники"])

@router.get("/industries")
def get_industries(db: Session = Depends(get_db)):
    return [{"id": i.id, "name": i.name} for i in db.query(Industry).all()]

@router.get("/sources")
def get_sources(db: Session = Depends(get_db)):
    return [{"id": s.id, "name": s.name} for s in db.query(DataSource).all()]