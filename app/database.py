import os
import aioredis
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs, AsyncSession

from dotenv import load_dotenv
load_dotenv()

# SQLALCHEMY POSTGRESQL
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


# # REDIS
# REDIS_HOST = os.getenv("REDIS_HOST")
# REDIS_PORT = int(os.getenv("REDIS_PORT"))

# redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT,
#                            db=0, decode_responses=True)


# async def create_redis_pool():
#     redis_pool = await aioredis.create_redis_pool((REDIS_HOST, REDIS_PORT))
#     return redis_pool
# try:
#     yield redis_pool
# finally:
#     redis_pool.close()
#     await redis_pool.wait_closed()


# async def close_redis_pool(redis_pool):
#     redis_pool.close()
#     await redis_pool.wait_closed()
