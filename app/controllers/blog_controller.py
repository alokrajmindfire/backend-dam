from sqlalchemy.orm import Session
from app.repositories.blog_repository import BlogRepository
from app.schemas.blog_schema import BlogCreate, BlogUpdate
from app.config.logger import logger

class BlogController:
    def __init__(self, db: Session):
        self.blog_repository = BlogRepository(db)

    def get_blogs(self):
        try:
            blogs = self.blog_repository.get_all()
            logger.info("Controller: returned all blogs.")
            return blogs
        except Exception as e:
            logger.error(f"Controller error in get_blogs: {e}")
            raise

    def get_blog(self, blog_id: int):
        try:
            blog = self.blog_repository.get_by_id(blog_id)
            if not blog:
                logger.warning(f"Controller: blog {blog_id} not found.")
            return blog
        except Exception as e:
            logger.error(f"Controller error in get_blog({blog_id}): {e}")
            raise

    def create_blog(self, blog_create: BlogCreate):
        try:
            logger.info(f"Controller: creating blog {blog_create.title}")
            return self.blog_repository.create(blog_create)
        except Exception as e:
            logger.error(f"Controller error in create_blog: {e}")
            raise

    def update_blog(self, blog_id: int, blog_update: BlogUpdate):
        try:
            blog = self.blog_repository.get_by_id(blog_id)
            if not blog:
                logger.warning(f"Controller: blog {blog_id} not found for update.")
                return None
            return self.blog_repository.update(blog, blog_update)
        except Exception as e:
            logger.error(f"Controller error in update_blog({blog_id}): {e}")
            raise

    def delete_blog(self, blog_id: int):
        try:
            blog = self.blog_repository.get_by_id(blog_id)
            if not blog:
                logger.warning(f"Controller: blog {blog_id} not found for deletion.")
                return None
            return self.blog_repository.delete(blog)
        except Exception as e:
            logger.error(f"Controller error in delete_blog({blog_id}): {e}")
            raise
