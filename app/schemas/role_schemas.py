from pydantic import BaseModel, ConfigDict

class RoleOut(BaseModel):
    id: int 
    role_name: str
    access_name: str

    model_config = ConfigDict(from_attributes=True)