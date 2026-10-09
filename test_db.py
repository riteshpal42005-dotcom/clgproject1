from sqlalchemy import text
from core.database import engine

with engine.connect() as conn:
    print(conn.execute(text("SELECT 1")).scalar())
    print("Supabase connected successfully!")
    