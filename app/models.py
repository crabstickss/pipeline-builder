from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Industry(Base):
    __tablename__ = "industries"
    __table_args__ = {'schema': 'public'}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))

class Scale(Base):
    __tablename__ = "scales"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))

class AnalysisGoal(Base):
    __tablename__ = "analysis_goals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))

class DataSource(Base):
    __tablename__ = "data_sources"
    __table_args__ = {'schema': 'public'}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))

class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    available_in_russia = Column(Boolean)
    description = Column(Text)
    budget_level = Column(String)

class GoalToolMap(Base):
    __tablename__ = "goal_tool_map"
    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer)
    tool_id = Column(Integer)

class DataBlock(Base):
    __tablename__ = 'data_blocks'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True)
    goal_id = Column(Integer, ForeignKey('analysis_goals.id'))
    stage = Column(String(100))
    tool = Column(String(100))               # добавлено
    source = Column(String(100))
    budget_level = Column(String(100))
    priority_order = Column(Integer) 
    description = Column(String(300))

class DataRequest(Base):
    __tablename__ = "user_requests"

    id = Column(Integer, primary_key=True, index=True)
    industry = Column(String(100))
    scale = Column(String(100))
    goal_id = Column(Integer, ForeignKey("analysis_goals.id"))
    budget_level = Column(String(100))
    timestamp = Column(String(100))