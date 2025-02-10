
from sqlalchemy.ext.declarative import  declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker , declarative_base


# DATABASE_URL= 'postgresql://{username}:{password}@localhost:{portnothatusedpostgresql}/{databaseName}'
DATABASE_URL = 'postgresql+asyncpg://postgres:test1234!@localhost:5433/aipolicing'
engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()



# Quick setup: create all tables based on your models.
async def init_db():
    async with engine.begin() as conn:
        # This will create all tables which do not yet exist.
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with async_session() as session:
        yield session
