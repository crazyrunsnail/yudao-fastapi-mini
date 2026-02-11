import asyncio
from sqlalchemy import text
from app.core.database import engine

async def init_notify_db():
    async with engine.begin() as conn:
        try:
            # 1. Create system_notify_template table
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS system_notify_template (
                    id BIGSERIAL PRIMARY KEY,
                    name VARCHAR(64) NOT NULL,
                    code VARCHAR(64) NOT NULL,
                    nickname VARCHAR(64) NOT NULL,
                    content TEXT NOT NULL,
                    type INTEGER NOT NULL,
                    params TEXT,
                    status SMALLINT DEFAULT 0,
                    remark VARCHAR(255),
                    creator VARCHAR(64) DEFAULT '',
                    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updater VARCHAR(64) DEFAULT '',
                    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    deleted SMALLINT DEFAULT 0,
                    tenant_id BIGINT DEFAULT 1
                );
            """))
            print("Table system_notify_template created/verified.")

            # 2. Create system_notify_message table
            # 注意：PostgreSQL 语法
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS system_notify_message (
                    id BIGSERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    user_type SMALLINT NOT NULL,
                    template_id BIGINT NOT NULL,
                    template_code VARCHAR(64) NOT NULL,
                    template_nickname VARCHAR(63) NOT NULL,
                    template_content TEXT NOT NULL,
                    template_type INTEGER NOT NULL,
                    template_params TEXT NOT NULL,
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
            
            # 3. Insert initial templates
            result = await conn.execute(text("SELECT count(*) FROM system_notify_template"))
            count = result.scalar()
            if count == 0:
                await conn.execute(text("""
                    INSERT INTO system_notify_template (name, code, nickname, content, type, params, status, remark) VALUES 
                    ('欢迎通知', 'welcome', '系统管理员', '欢迎 #{nickname} 加入系统！', 1, '["nickname"]', 0, '新用户入驻通知'),
                    ('安全提醒', 'security', '安全中心', '您的账号于 #{time} 在 #{location} 登录，如非本人操作请及时更新密码。', 2, '["time", "location"]', 0, '异地登录提醒')
                """))
                print("Initial templates inserted.")

            # 4. Insert mock data if empty
            result = await conn.execute(text("SELECT count(*) FROM system_notify_message"))
            count = result.scalar()
            if count == 0:
                # 假设 user_id=1 是当前登录用户（admin）
                await conn.execute(text("""
                    INSERT INTO system_notify_message (user_id, user_type, template_id, template_code, template_nickname, template_content, template_type, template_params, read_status, create_time, tenant_id) VALUES 
                    (1, 1, 1, 'welcome', '系统通知', '欢迎使用本系统', 1, '{}', false, NOW(), 1),
                    (1, 1, 2, 'security', '安全提醒', '您的密码即将过期，请及时修改', 2, '{}', false, NOW(), 1);
                """))
                print("Mock messages inserted.")
            else:
                print(f"Table system_notify_message already has {count} records.")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(init_notify_db())
