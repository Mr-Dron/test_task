from pydantic import BaseModel, ConfigDict

class RoleOut(BaseModel):
    id: int 
    role_name: str
    access_level: int

    model_config = ConfigDict(from_attributes=True)