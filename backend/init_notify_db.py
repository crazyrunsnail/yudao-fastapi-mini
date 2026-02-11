import asyncio
from sqlalchemy import text
from app.core.database import engine

async def init_notify_table():
    async with engine.begin() as conn:
        try:
            # Create table
            # 注意：PostgreSQL 语法
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS system_notify_message (
                    id BIGSERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    user_type SMALLINT NOT NULL,
                    template_id BIGINT NOT NULL,
                    template_code VARCHAR(64) NOT NULL,
                    template_nickname VARCHAR(63) NOT NULL,
                    template_content VARCHAR(1024) NOT NULL,
                    template_type INTEGER NOT NULL,
                    template_params VARCHAR(255) NOT NULL,
                    read_status BOOLEAN NOT NULL DEFAULT FALSE,
                    read_time TIMESTAMP,
                    creator VARCHAR(64) DEFAULT '',
                    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updater VARCHAR(64) DEFAULT '',
                    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    deleted SMALLINT DEFAULT 0,
                    tenant_id BIGINT DEFAULT 1
                );
            """))
            print("Table system_notify_message created/verified.")
            
            # Insert mock data if empty
            result = await conn.execute(text("SELECT count(*) FROM system_notify_message"))
            count = result.scalar()
            if count == 0:
                # 假设 user_id=1 是当前登录用户（admin）
                await conn.execute(text("""
                    INSERT INTO system_notify_message (user_id, user_type, template_id, template_code, template_nickname, template_content, template_type, template_params, read_status, create_time, tenant_id) VALUES 
                    (1, 1, 1, 'welcome', '系统通知', '欢迎使用本系统', 1, '{}', false, NOW(), 1),
                    (1, 1, 2, 'security', '安全提醒', '您的密码即将过期，请及时修改', 2, '{}', false, NOW(), 1);
                """))
                print("Mock data inserted.")
            else:
                print(f"Table already has {count} records.")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(init_notify_table())
