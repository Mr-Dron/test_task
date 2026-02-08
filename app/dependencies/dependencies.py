from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

from datetime import datetime, timezone

from typing import TypeVar, Type

from app.db.database import AsyncSessionLocal, Base
from app.models import Users, Tokens
from app.config.security import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")
ModelType = TypeVar("ModelType", bound=Base)

# контекст менеджер сессии
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal () as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

# получение текущего пользователя 
async def get_current_user(token: str=Depends(oauth2_scheme),
                           db: AsyncSession=Depends(get_session)) -> Users:

    payload = verify_access_token(token)
    
    user_id = payload["sub"]

    current_user = (await db.execute(select(Users).where(Users.id == user_id))).scalar_one_or_none()

    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="User is not active")

    return current_user

#получение текущего пользователя с обновлением активности
def get_current_user_with_activity():
    async def dependency(user: Users=Depends(get_current_user),
                         db: AsyncSession=Depends(get_session)):
        await update_last_seen(user=user, db=db)
        return user
    return dependency

#обновление активности пользователя
async def update_last_seen(user: Users, db: AsyncSession):

    user.last_seen = datetime.now(timezone.utc)

    db.add(user)
    await db.commit()

    return {"message", "ok"}

#фабрика зависимостей на изменение состояние пользователя
def set_user_status(state: bool):
    async def inner(user: Users=Depends(get_current_user),
                    db: AsyncSession=Depends(get_session)):
        
        if user.online != state:
            user.online = state

            db.add(user)
            await db.commit()
            
        return {"message": "ok"} 
    return inner

def entity_activity_check(id_field: str, entity: Type[ModelType]):
    async def checker(db: AsyncSession=Depends(get_session),
                      **path_params):
        
        entity_id = path_params[id_field]

        stmt = (select(entity)
                .where(and_(
                    entity.id == entity_id,
                    entity.is_active.is_(True)
                )))
        
        result = (await db.execute(stmt)).scalar_one_or_none()

        if not result:
            raise HTTPException(status_code=400, detail=f"Entity {entity.__name__} is not active")


    return checker