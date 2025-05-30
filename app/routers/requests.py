from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(
    prefix="/request",
    tags=["Request"]
)

# временное хранилище в памяти
requests_db = []

# модель данных запроса
class RequestData(BaseModel):
    industry: str
    scale: str
    goal_id: int
    budget: str
    selected_sources: Optional[List[str]] = []

@router.post("/")
def save_request(data: RequestData):
    request_id = len(requests_db) + 1
    saved = {"id": request_id, **data.dict()}
    requests_db.append(saved)
    return {"message": "Запрос сохранён", "id": request_id}

@router.get("/{request_id}")
def get_request(request_id: int):
    for r in requests_db:
        if r["id"] == request_id:
            return r
    return {"detail": "Запрос не найден"}
@router.get("/")
def get_all_requests():
    return requests_db