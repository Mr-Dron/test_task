from pydantic import BaseModel, ConfigDict
from typing import Optional

from app.validatos.schemas_validators.value_validators import ValueValidatorMixin

class PostCreate(BaseModel, ValueValidatorMixin):
    title: str
    description: Optional[str] = None

class PostUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class PostOutFull(BaseModel):

    id: int
    title: str
    description: Optional[str] = None
    likes: int

    creator_id: int
    group_id: int

    model_config = ConfigDict(from_attributes=True)