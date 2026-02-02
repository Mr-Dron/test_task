from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from fastapi import Depends, HTTPException

from app.models import *
from app.dependencies.dependencies import get_session, get_current_user


def check_permission(access_level: int):
    async def checker(group_id: int,
                      user: Users=Depends(get_current_user),
                      db: AsyncSession=Depends(get_session)):
        
        stmt = (
            select(Roles)
            .join(Roles.groups_members)
            .where(and_(GroupMembers.group_id == group_id,
                        GroupMembers.user_id == user.id))
        )

        role = (await db.execute(stmt)).scalar_one_or_none()

        if not role:
            raise HTTPException(status_code=404, detail="Not found")
        
        if role.access_level < access_level:
            raise HTTPException(status_code=403, detail="Permission denied")

    return checker