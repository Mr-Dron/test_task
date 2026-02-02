from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Roles

async def get_all_roles(db: AsyncSession):
    
    roles = (await db.execute(select(Roles))).scalars().all()

    return roles