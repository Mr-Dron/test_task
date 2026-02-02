from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastapi import HTTPException

from app.models import Users

async def get_user_by_email(user_email: str, db: AsyncSession):

    stmt = (
        select(Users)
        .where(Users.email == user_email)
    )

    user = (await db.execute(stmt)).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail=f"User with email={user_email} not found")
    
    return user