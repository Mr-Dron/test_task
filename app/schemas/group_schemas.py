from pydantic import BaseModel, ConfigDict
from typing import Optional

from datetime import datetime

from app.validatos.schemas_validators.value_validators import ValueValidatorMixin

class GroupCreate(BaseModel, ValueError):
    title: str
    description: Optional[str] = None

class GroupUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class GroupAddMember(BaseModel):
    email: Optional[str] = None
    id: Optional[str] = None
    role_id: int 

class GroupOutFull(BaseModel):

    id: int
    title: str
    description: Optional[str] = None
    create_at: datetime
    creator_id: int

    model_config = ConfigDict(from_attributes=True)