from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, APIRouter, status

from app.schemas import *
from app.models import *
from app.services import group_service
from app.dependencies.dependencies import get_current_user, get_session
from app.dependencies.permissions_validators import check_permission

router = APIRouter(prefix="/groups", tags=["Groups"])

# Создание группы
@router.post("/", response_model=group_schemas.GroupOutFull, status_code=status.HTTP_201_CREATED)
async def create_group(group_data: group_schemas.GroupCreate, current_user: Users=Depends(get_current_user), db: AsyncSession=Depends(get_session)):
    return await group_service.group_create(group_data=group_data, current_user=current_user, db=db)

# Добавление участников в группу
@router.post("/{group_id}/add_member/", status_code=status.HTTP_200_OK, 
             dependencies=[Depends(check_permission(2))])
async def add_member(group_id: int, member_data: group_schemas.GroupAddMember, db: AsyncSession=Depends(get_session)):
    return await group_service.add_member(group_id=group_id, user_data=member_data, db=db)

# Обновление группы
@router.put("/{group_id}/", response_model=group_schemas.GroupOutFull, 
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(check_permission(3))])
async def update_group(group_id: int, group_data: group_schemas.GroupUpdate, db: AsyncSession=Depends(get_session)):
    return await group_service.group_update(group_id=group_id, group_data=group_data, db=db)

# Удаление группы
@router.delete("/{group_id}/", status_code=status.HTTP_200_OK, 
               dependencies=[Depends(check_permission(3))])
async def delete_group(group_id: int, db: AsyncSession=Depends(get_session)):
    return await group_service.delete_group(group_id=group_id, db=db)

