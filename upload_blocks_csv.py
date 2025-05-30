import psycopg2

conn = psycopg2.connect(
    dbname="pipeline_db",
    user="postgres",
    password="Edward1914",
    host="localhost",
    port="5433"
)

cur = conn.cursor()

# Очистим таблицу
cur.execute("TRUNCATE TABLE data_blocks RESTART IDENTITY;")

with open("C:/Users/MargoRitta/Documents/blocks.csv", "r", encoding="utf-8") as f:
    next(f)  # Пропустить заголовки
    cur.copy_expert("""
        COPY data_blocks(goal_id, stage, budget_level, description, source, tool, priority_order)
        FROM STDIN WITH CSV DELIMITER ',' NULL '' QUOTE '"' ESCAPE '"'
    """, f)

conn.commit()
cur.close()
conn.close()

print("✅ Данные загружены успешно!")
