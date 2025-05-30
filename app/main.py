from fastapi import FastAPI
from app.database import SessionLocal
from app.models import DataBlock
from app.routers.goals import router as goals_router
from app.routers.tools import router as tools_router
from app.routers.sources import router as sources_router
from app.routers.blocks import router as blocks_router
from app.routers.requests import router as requests_router
from app.models import Base, DataBlock
from app.routers.recommendations import router as recommendations_router
from app.routers.dictionaries import router as dicts_router
from app.models import Tool
from app.models import Base
from app.database import engine
# -*- coding: utf-8 -*-
 
Base.metadata.create_all(bind=engine)
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 или укажи конкретный адрес, если нужно ограничение
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(goals_router)
app.include_router(dicts_router)
app.include_router(tools_router)
app.include_router(blocks_router)
app.include_router(sources_router)
app.include_router(requests_router)
app.include_router(recommendations_router)
 


db = SessionLocal()

try:
    rows = db.query(DataBlock).limit(5).all()
    for r in rows:
        print(r.id, r.stage)
except Exception as e:
    print("❌ Ошибка:", e)
finally:
    db.close()
@app.get("/")
def read_root():
    return {"message": "Бэкенд конструктора пайплайнов работает!"}