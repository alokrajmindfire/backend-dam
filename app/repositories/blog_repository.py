from sqlalchemy.orm import Session
from app.models.blog_model import Blog
from app.schemas.blog_schema import BlogCreate, BlogUpdate
from app.config.logger import logger
from fastapi import HTTPException, status

class BlogRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        try:
            blogs = self.db.query(Blog).all()
            logger.info("Fetched all blogs from database.")
            return blogs
        except Exception as e:
            logger.exception(f"Error fetching blogs: {e}")
            raise

    def get_by_id(self, blog_id: int):
        try:
            blog = self.db.query(Blog).filter(Blog.id == blog_id).first()
            if not blog:
                logger.warning(f"Blog with id {blog_id} not found.")
            return blog
        except Exception as e:
            logger.exception(f"Error fetching blog {blog_id}: {e}")
            raise

    def create(self, blog_create: BlogCreate):
        try:
            existing_blog = self.db.query(Blog).filter(Blog.slug == blog_create.slug).first()
            if existing_blog:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Blog with slug '{blog_create.slug}' already exists"
                )
            blog = Blog(
                title=blog_create.title,
                slug=blog_create.slug,
                content=blog_create.content,
                author_id=blog_create.author_id,
                is_active=blog_create.is_active
            )
            self.db.add(blog)
            self.db.commit()
            self.db.refresh(blog)
            logger.info(f"Blog created successfully: {blog.title}")
            return blog
        except Exception as e:
            self.db.rollback()
            logger.exception(f"Error creating blog {blog_create.title}: {e}")
            raise

    def update(self, blog: Blog, blog_update: BlogUpdate):
        try:
            for key, value in blog_update.dict(exclude_unset=True).items():
                setattr(blog, key, value)
            self.db.commit()
            self.db.refresh(blog)
            logger.info(f"Blog updated successfully: {blog.id}")
            return blog
        except Exception as e:
            self.db.rollback()
            logger.exception(f"Error updating blog {blog.id}: {e}")
            raise

    def delete(self, blog: Blog):
        try:
            self.db.delete(blog)
            self.db.commit()
            logger.info(f"Blog deleted successfully: {blog.id}")
            return blog
        except Exception as e:
            self.db.rollback()
            logger.exception(f"Error deleting blog {blog.id}: {e}")
            raise
