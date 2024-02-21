from app.database import SessionLocal
from app.models import User
from app.data.fake_users import FAKE_USERS
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def initialize_fake_users():
    db = SessionLocal()

    for user_data in FAKE_USERS:
        # Check if username already exists
        existing_user = (await db.execute(select(User).where(User.userName == user_data["userName"]))).first()
        if existing_user is None:
            # async with AsyncSession(db) as async_session:
            async with db as async_session:
                new_user = User(
                    userName=user_data["userName"],
                    fullName=user_data["fullName"],
                    email=user_data["email"],
                    hashedPassword=user_data["hashedPassword"],
                    dob=None,
                    gender=user_data["gender"],
                    createdAt=user_data["createdAt"],
                    updatedAt=user_data["updatedAt"]
                )
                async_session.add(new_user)
                await async_session.commit()
                await async_session.refresh(new_user)
