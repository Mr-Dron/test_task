from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastapi import HTTPException

from app.models import Roles


async def get_role_creator_id(db: AsyncSession):

    stmt = (select(Roles.id)
            .where(Roles.role_name == "creator"))
    
    role_id = (await db.execute(stmt)).scalar_one_or_none()

    if not role_id:
        raise HTTPException(status_code=404, detail="Role not found")
    
    return role_id