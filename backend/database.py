from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from config import get_settings
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

settings = get_settings()
SQLALCHEMY_DATABASE_URL = (
	"mysql+aiomysql://"
	f"{settings.database_username}:{settings.database_password}"
	f"@db:{settings.database_port}/newsletter_schema"
)
engine: AsyncEngine = create_async_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = async_sessionmaker(
	class_=AsyncSession,
	autocommit=False,
	autoflush=False,
	expire_on_commit=False,
	bind=engine
)


class Base(AsyncAttrs, DeclarativeBase):
    pass

