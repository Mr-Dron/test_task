from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from fastapi import HTTPException

from datetime import datetime, timezone

from app.models import Groups, Users, GroupMembers
from app.schemas import group_schemas
from app.services.helpers import group_helpers, user_helpers
from app.dependencies.dependencies import entity_activity_check


async def group_create(group_data: group_schemas.GroupCreate, current_user: Users, db: AsyncSession):

    data = group_data.model_dump()
    data["create_at"] = datetime.now(timezone.utc)
    data["creator_id"] = current_user.id
    data["is_active"] = True

    new_group = Groups(**data)

    db.add(new_group)

    await db.flush()
    await db.refresh(new_group)

    role_id = await group_helpers.get_role_creator_id(db=db)
    user_data = group_schemas.GroupAddMember(id=current_user.id,
                                             role_id=role_id)
    await add_member(group_id=new_group.id, user_data=user_data, db=db)

    return new_group

async def group_update(group_id: int, group_data: group_schemas.GroupUpdate, db: AsyncSession):

    new_data = group_data.model_dump(exclude_unset=True)

    stmt = (
        update(Groups).
        values(**new_data)
        .where(Groups.id == group_id)
        .returning(Groups)
    )

    updated_group = (await db.execute(stmt)).scalar_one_or_none()

    if not updated_group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    return updated_group


async def add_member(group_id: int, user_data: group_schemas.GroupAddMember, db: AsyncSession):

    if user_data.email:
        user = await user_helpers.get_user_by_email(user_email=user_data.email, db=db)
        user_data.id = user.id

    await entity_activity_check(id_field="user_id", entity=Users)(db=db, user_id=user_data.id)

    if not user_data.id:
        raise HTTPException(status_code=400, detail="Parameters not passed")

    new_member = GroupMembers(group_id=group_id,
                              user_id=user_data.id,
                              role_id=user_data.role_id)
    
    db.add(new_member)

    return {"message": "ok"}


async def delete_group(group_id: int, db: AsyncSession):

    stmt = (
        update(Groups)
        .where(Groups.id == group_id)
        .values(is_active = False,
                delete_at = datetime.now(timezone.utc))
        .returning(Groups)
    )

    deleted_group = (await db.execute(stmt)).scalar_one_or_none()

    if not deleted_group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    return {"message": "group deleted successfully"}