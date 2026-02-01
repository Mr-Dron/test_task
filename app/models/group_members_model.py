from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey

from app.db.database import Base

class GroupMembers(Base):
    __tablename__ = "group_members"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"))
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"))

    user = relationship("Users", back_populates="groups_roles")
    group = relationship("Groups", back_populates="members_roles")
    role = relationship("Roles", back_populates="groups_members")