import os
from dotenv import load_dotenv
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('POSTGRESQL_ADDON_USER')}:{os.getenv('POSTGRESQL_ADDON_PASSWORD')}"
    f"@{os.getenv('POSTGRESQL_ADDON_HOST')}:{os.getenv('POSTGRESQL_ADDON_PORT')}/"
    f"{os.getenv('POSTGRESQL_ADDON_DB')}"
)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)