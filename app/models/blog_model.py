from datetime import datetime
from sqlalchemy import Column, Integer, Text, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Blog(Base):
    __tablename__ = "blogs"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    author_id =  Column(Integer,ForeignKey("users.id"))
    author = relationship("User",back_populates="blogs")
    created_at = Column(DateTime, default=datetime.now)
