from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    
    code_files = relationship("CodeFile", back_populates="owner")

class CodeFile(Base):
    __tablename__ = "code_files"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    content = Column(Text, default="")
    owner_id = Column(String, ForeignKey("users.id"))

    owner = relationship("User", back_populates="code_files")

class EditingSession(Base):
    __tablename__ = "editing_sessions"

    id = Column(String, primary_key=True, index=True)
    file_id = Column(String, ForeignKey("code_files.id"))
    user_id = Column(String, ForeignKey("users.id"))
    cursor_position = Column(Text, default='{"lineNumber": 1, "column": 1}')
    last_updated = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    file = relationship("CodeFile")
