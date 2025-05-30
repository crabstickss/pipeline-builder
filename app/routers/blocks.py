from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import DataBlock
from app.dependencies import get_db

router = APIRouter(prefix="/blocks", tags=["Блоки анализа"])

@router.get("/")
def get_blocks(db: Session = Depends(get_db)):
    try:
        blocks = db.query(DataBlock).limit(5).all()
        return blocks
    except Exception as e:
        return {"error": str(e)}


