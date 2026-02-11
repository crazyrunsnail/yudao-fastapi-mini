# Database SQL Files

This directory contains the SQL files for initializing and updating the database.

## Structure

*   `init.sql`: The main initialization script. **This is the Source of Truth for the database schema.**
    *   Copied from `yudao-boot-mini/sql/postgresql/ruoyi-vue-pro.sql` initially.
    *   Edit this file directly to modify the initial schema or data.

## Usage

### Initialize Database

To reset and initialize the database, execute the initialization script from the project root:

```bash
python scripts/init_db.py
```

This script will automatically detect `sql/init.sql` and execute it.

### Applying Updates

For incremental updates, you can create new `.sql` files in this directory (e.g., `update_20240101.sql`) and run them manually or via a custom script.

If you are using Alembic for migrations but want to execute raw SQL, you can use `op.execute(sql_content)` in your migration files.
