from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import text
from app.database.connection import Base
import app.models.user
import app.models.profile
import app.models.character
import app.models.career
import app.models.research
import app.models.integration
import app.models.education
import app.models.social
import app.models.notebook

ALTER_COLUMNS = [
    # users table alterations
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS account_type VARCHAR(50);",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_verified BOOLEAN DEFAULT TRUE;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS verification_token VARCHAR(255);",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_password_token VARCHAR(255);",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token_expiry TIMESTAMP;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS profile_completed BOOLEAN DEFAULT FALSE;",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS first_time_login BOOLEAN DEFAULT TRUE;",

    # user_profiles table alterations
    "ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS phone_number VARCHAR(50);",
    "ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS date_of_birth VARCHAR(50);",
    "ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS country VARCHAR(100);",
    "ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS state VARCHAR(100);",
    "ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS city VARCHAR(100);",
    "ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS avatar_url VARCHAR(1000);",
    "ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS profession VARCHAR(100);",
    "ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS organization VARCHAR(255);",
    "ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS enabled_modules JSONB DEFAULT '[\"study\", \"career\", \"research\", \"creator\", \"planner\", \"knowledge_base\"]'::jsonb;",
    "ALTER TABLE user_profiles ALTER COLUMN native_language DROP NOT NULL;",
    "ALTER TABLE user_profiles ALTER COLUMN english_level DROP NOT NULL;",

    # research_notes alterations
    "ALTER TABLE research_notes ALTER COLUMN research_project_id DROP NOT NULL;",
    "ALTER TABLE research_notes ADD COLUMN IF NOT EXISTS notebook_id UUID REFERENCES research_notebooks(id) ON DELETE CASCADE;",
    "ALTER TABLE research_notes ADD COLUMN IF NOT EXISTS category VARCHAR(100) DEFAULT 'General';"
]

async def run_database_migrations(engine: AsyncEngine):
    async with engine.begin() as conn:
        # 1. Apply column alterations to existing tables
        for sql in ALTER_COLUMNS:
            try:
                await conn.execute(text(sql))
            except Exception as e:
                print(f"Migration notice for '{sql}': {e}")
        
        # 2. Create any missing tables defined in Base metadata
        await conn.run_sync(Base.metadata.create_all)
        print("Database schema migration completed successfully.")
