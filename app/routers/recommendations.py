from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import Tool, DataSource, DataBlock, GoalToolMap
from app.dependencies import get_db
from pydantic import BaseModel
from fastapi import HTTPException
from app.models import Tool
from sqlalchemy import func


router = APIRouter(prefix="/recommendations", tags=["Рекомендации"])

class RecommendationInput(BaseModel):
    goal_id: int
    industry: str
    scale: str
    budget_level: str
    sources: List[str]


@router.get("/tool_info/{tool_name}")
def get_tool_info(tool_name: str, db: Session = Depends(get_db)):
    tool = db.query(Tool).filter(func.lower(Tool.name) == tool_name.lower()).first()
    if not tool:
        raise HTTPException(status_code=404, detail="Инструмент не найден")

    return {
        "name": tool.name,
        "description": tool.description or "Нет описания",
        "available_in_russia": tool.available_in_russia,
        "site": tool.site or "Не указан"
    }

@router.post("/")
def get_recommendations(data: RecommendationInput, db: Session = Depends(get_db)):
    try:
        print("🚀 Получены данные:", data.dict())

        # 1. Инструменты по цели
        tool_ids = db.query(GoalToolMap.tool_id).filter(GoalToolMap.goal_id == data.goal_id).all()
        tool_ids = [t[0] for t in tool_ids]
        print("🔧 tool_ids:", tool_ids)

        tools = db.query(Tool).filter(Tool.id.in_(tool_ids))

        # 🎯 Фильтрация только инструментов по бюджету
        if data.budget_level:
            tools = tools.filter(Tool.budget_level == data.budget_level)

        tools = tools.filter(Tool.available_in_russia == True)
        selected_tools = tools.all()
        print("✅ Найдено инструментов:", len(selected_tools))

        # 2. Этапы анализа по цели (без фильтрации по бюджету)
        blocks = db.query(DataBlock).filter(DataBlock.goal_id == data.goal_id).all()
        print("📦 Найдено блоков:", len(blocks))

        # 3. Источники из блоков
        sources_from_blocks = list({
            b.source.strip() for b in blocks
            if b.source and b.source.strip().lower() != "не требуются"
        })
        print("🛁 Источники из блоков:", sources_from_blocks)

        return {
            "tools": [f"{tool.name}::{tool.category}" for tool in selected_tools],
            "sources": sources_from_blocks,
            "blocks": [{"stage": b.stage, "description": b.description} for b in blocks]
        }

    except Exception as e:
        print("❌ Ошибка в /recommendations/:", e)
        return {"error": str(e)}
@router.get("/tool_info/{tool_name}")
def get_tool_info(tool_name: str, db: Session = Depends(get_db)):
    tool = db.query(Tool).filter(Tool.name == tool_name).first()
    if not tool:
        return {"error": "Инструмент не найден"}

    return {
        "name": tool.name,
        "description": tool.description,
        "available_in_russia": tool.available_in_russia,
        #"website": tool.website
    }