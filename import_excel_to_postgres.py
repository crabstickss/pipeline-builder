import pandas as pd
from sqlalchemy import create_engine

# Подключение к PostgreSQL
DATABASE_URL = "postgresql://postgres:Edward1914@localhost:5433/pipeline_db"
engine = create_engine(DATABASE_URL)

excel_path = "C:/Users/MargoRitta/Documents/Конструктор пайплайнов (2).xlsx"

# 1. ЦЕЛИ АНАЛИЗА 
df_goals = pd.read_excel(excel_path, sheet_name="Цели_анализа")
df_goals = df_goals.rename(columns={"Цели": "name"})
df_goals["id"] = range(1, len(df_goals) + 1)
df_goals = df_goals[["id", "name"]]
df_goals.to_sql("analysis_goals", con=engine, if_exists="replace", index=False)
print(" Цели анализа загружены.")
df_industries = pd.read_excel(excel_path, sheet_name="Отрасли")  
df_industries = df_industries.rename(columns={"Отрасль": "name"})  
df_industries["id"] = range(1, len(df_industries) + 1)
df_industries = df_industries[["id", "name"]]
df_industries.to_sql("industries", con=engine, if_exists="replace", index=False)
print(" Отрасли загружены.")
# 2. ИСТОЧНИКИ ДАННЫХ
df_sources = pd.read_excel(excel_path, sheet_name="Источники_данных")
df_sources = df_sources.rename(columns={"Категория источника данных": "name"})
df_sources["id"] = range(1, len(df_sources) + 1)
df_sources = df_sources[["id", "name"]]
df_sources.to_sql("data_sources", con=engine, if_exists="replace", index=False)
print("✅ Источники данных загружены.")

# 3. ИНСТРУМЕНТЫ
df_tools = pd.read_excel(excel_path, sheet_name="Инструменты")
df_tools = df_tools.rename(columns={
    "Название инструмента": "name",
    "Категория": "category",
    "Описание": "description",
    "Бюджет": "budget_level",
    "Доступен в РФ": "available_in_russia",
    "Ссылка на сайт": "site"
})
if "available_in_russia" not in df_tools.columns:
    df_tools["available_in_russia"] = True
df_tools["id"] = range(1, len(df_tools) + 1)
df_tools = df_tools[["id", "name", "category", "description", "budget_level", "available_in_russia"]]
df_tools.to_sql("tools", con=engine, if_exists="replace", index=False)
print(" Инструменты загружены.")


#4. БЛОКИ 
df_blocks = pd.read_excel(excel_path, sheet_name="Блоки_управления_данными")
df_blocks = df_blocks.rename(columns={
    "goal_id": "goal_id",
    "Тип блока": "stage",
    "Бюджет": "budget_level",
    "Основное описание": "description",
    "Источники данных (рекомендуемые)": "source",
    "Инструмент": "tool",
    "Порядок приоритета": "priority_order"
})

# Заполнить отсутствующие поля по умолчанию
if "tool" not in df_blocks.columns:
    df_blocks["tool"] = None
if "priority_order" not in df_blocks.columns:
    df_blocks["priority_order"] = 0

df_blocks["id"] = range(1, len(df_blocks) + 1)
df_blocks = df_blocks[["id", "goal_id", "stage", "tool", "source", "budget_level", "priority_order", "description"]]
df_blocks.to_sql("data_blocks", con=engine, if_exists="replace", index=False)
print(" Блоки загружены.")

df_map = pd.read_excel(excel_path, sheet_name="Цель_инструмент")

df_map = df_map.rename(columns={
    "Инструмент": "tool_name",
    "Цель анализа": "goal_name"
})

df_goals = pd.read_sql("SELECT id, name FROM analysis_goals", con=engine)
df_tools = pd.read_sql("SELECT id, name FROM tools", con=engine)

df_map = df_map.merge(df_goals, left_on="goal_name", right_on="name") \
               .merge(df_tools, left_on="tool_name", right_on="name", suffixes=("_goal", "_tool"))

df_final = df_map[["id_goal", "id_tool"]]
df_final.columns = ["goal_id", "tool_id"]
df_final = df_final.copy()
df_final["id"] = range(1, len(df_final) + 1)
df_final = df_final[["id", "goal_id", "tool_id"]]

df_final.to_sql("goal_tool_map", con=engine, if_exists="replace", index=False)
print("Цель–Инструмент загружены.")
df_requests = pd.read_excel(excel_path, sheet_name="User_input")  

df_requests = pd.read_excel(excel_path, sheet_name="User_input")  

df_requests = df_requests.rename(columns={
    "Email": "email",
    "Отрасль": "industry",
    "Масштаб": "scale",
    "Бюджет": "budget_level",
    "Цель анализа": "goal_name"
})

# Загружаем справочник целей
df_goals = pd.read_sql("SELECT id, name FROM analysis_goals", con=engine)

# Соединяем с целями по названию
df_requests = df_requests.merge(df_goals, left_on="goal_name", right_on="name")

# Добавляем timestamp
df_requests["timestamp"] = pd.Timestamp.now()

# Оставляем нужные поля
df_requests = df_requests[["email", "industry", "scale", "budget_level", "id", "timestamp"]]
df_requests.columns = ["email", "industry", "scale", "budget_level", "goal_id", "timestamp"]

# Загружаем в БД
df_requests.to_sql("user_requests", con=engine, if_exists="append", index=False)

print(" Запросы пользователей успешно загружены.")