#!/usr/bin/env python3
import asyncio
import os
import sys
import re
from pathlib import Path

# Add backend directory to sys.path
# This allows 'from app.core.database import engine' to work
backend_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(backend_dir))

from sqlalchemy import text
from app.core.database import engine

async def init_db(sql_file_path):
    if not os.path.exists(sql_file_path):
        print(f"Error: SQL file not found at {sql_file_path}")
        return

    print(f"Initializing database from {sql_file_path}...")
    
    with open(sql_file_path, "r", encoding="utf-8") as f:
        sql_content = f.read()

    # 1. Clean up transaction control commands aggressively
    # The regex matches BEGIN or COMMIT followed by ; with optional whitespace
    sql_content = re.sub(r'^\s*BEGIN\s*;\s*$', '', sql_content, flags=re.MULTILINE | re.IGNORECASE)
    sql_content = re.sub(r'^\s*COMMIT\s*;\s*$', '', sql_content, flags=re.MULTILINE | re.IGNORECASE)

    # 2. Use engine.begin() for a direct connection transaction
    # This bypasses session overhead and usually handles multi-statement scripts better in raw mode
    try:
        async with engine.begin() as conn:
            await conn.execute(text(sql_content))
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    backend_dir = Path(__file__).resolve().parent.parent
    # Check multiple possible locations for the SQL file
    possible_paths = [
        backend_dir / "sql/init.sql",
        backend_dir.parent / "yudao-boot-mini/sql/postgresql/ruoyi-vue-pro.sql",
    ]
    
    target_sql = None
    if len(sys.argv) > 1:
        target_sql = sys.argv[1]
    else:
        for p in possible_paths:
            if p.exists():
                target_sql = str(p)
                break
    
    if target_sql:
        asyncio.run(init_db(target_sql))
    else:
        print("Error: No SQL file found. Please specify one as an argument.")
