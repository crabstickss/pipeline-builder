from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.dependencies import get_db
from app.models import Tool, GoalToolMap

router = APIRouter(prefix="/tools", tags=["Инструменты"])

@router.get("/")
def get_tools(
    goal_id: int = Query(...),
    budget: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    # JOIN: связываем tools с goal_tool_map
    query = db.query(Tool).join(GoalToolMap, Tool.id == GoalToolMap.tool_id)\
        .filter(GoalToolMap.goal_id == goal_id)

    if budget:
        query = query.filter(Tool.budget_level == budget)

    if source:
        query = query.filter(Tool.source_type == source)

    return query.all()
@router.get("/tools/{tool_name}")
def get_tool_by_name(tool_name: str, db: Session = Depends(get_db)):
    tool = db.query(Tool).filter(Tool.name == tool_name).first()
    if not tool:
        return {"error": "Tool not found"}

    return {
        "name": tool.name,
        "description": tool.description,
        "available_in_russia": tool.available_in_russia,
        "website": tool.website
    }