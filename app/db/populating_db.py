from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Roles

async def filling_db(db: AsyncSession):

    roles_list = [
        {"role_name": "creator", "access_level": 3},
        {"role_name": "admin", "access_level": 2},
        {"role_name": "member", "access_level": 1}
    ]

    roles = (await db.execute(select(Roles))).scalars().all()

    if not roles:
        for role_data in roles_list:
            new_role = Roles(**role_data)
            db.add(new_role)
        
    
    await db.commit()