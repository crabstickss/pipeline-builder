from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import AnalysisGoal
from app.dependencies import get_db

router = APIRouter(prefix="/goals", tags=["Цели анализа"])

@router.get("/")
def get_goals(db: Session = Depends(get_db)):
    return db.query(AnalysisGoal).all()