from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey

from app.db.database import Base

class Roles(Base):
    __tablename__ = "roles"

    role_name = Column(String(50), nullable=False)
    access_level = Column(Integer, nullable=False)


    groups_members = relationship("GroupMembers", back_populates="role")