from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class BlogBase(BaseModel):
    title: str
    slug: str
    content: Optional[str] = None

class BlogCreate(BlogBase):
    pass

class BlogUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None

class BlogResponse(BlogBase):
    id: int
    author_id: int
    created_at: datetime
