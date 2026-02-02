from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, status, Depends

from app.dependencies.dependencies import get_session
from app.schemas import role_schemas
from app.services import role_service

router = APIRouter("/roles", tags=["Roles"])

@router.get("/", response_model=list[role_schemas.RoleOut], status_code=status.HTTP_200_OK)
async def get_roles(db: AsyncSession=Depends(get_session)):
    return await role_service.get_all_roles(db=db)