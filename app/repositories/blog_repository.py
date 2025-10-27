from sqlalchemy.orm import Session
from app.models.blog_model import Blog
from app.schemas.blog_schema import BlogCreate, BlogUpdate
from app.config.logger import logger
from fastapi import HTTPException, status

class BlogRepository:
    """
    Repository class for performing CRUD operations on the Blog model.
    """
    def __init__(self, db: Session):
        """
        Initialize the BlogRepository with a database session.

        Args:
            db (Session): SQLAlchemy database session.
        """
        self.db = db

    def get_all(self):
        """
        Retrieve all blogs from the database.

        Returns:
            list[Blog]: A list of all Blog objects.

        Raises:
            Exception: If a database or query error occurs.
        """
        try:
            blogs = self.db.query(Blog).all()
            logger.info("Fetched all blogs from database.")
            return blogs
        except Exception as e:
            logger.exception(f"Error fetching blogs: {e}")
            raise

    def get_by_id(self, blog_id: int):
        """
        Retrieve a single blog by its ID.

        Args:
            blog_id (int): The ID of the blog to retrieve.

        Returns:
            Blog | None: The Blog object if found, otherwise None.

        Raises:
            Exception: If a database or query error occurs.
        """
        try:
            blog = self.db.query(Blog).filter(Blog.id == blog_id).first()
            if not blog:
                logger.warning(f"Blog with id {blog_id} not found.")
            return blog
        except Exception as e:
            logger.exception(f"Error fetching blog {blog_id}: {e}")
            raise

    def create(self, blog_create: BlogCreate):
        """
        Create a new blog entry in the database.

        Args:
            blog_create (BlogCreate): The data required to create a new blog.

        Returns:
            Blog: The newly created Blog object.

        Raises:
            HTTPException: If a blog with the same slug already exists.
            Exception: If there’s an unexpected error during creation.
        """
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
        """
        Update an existing blog entry.

        Args:
            blog (Blog): The existing Blog object to update.
            blog_update (BlogUpdate): The data to update the blog with.

        Returns:
            Blog: The updated Blog object.

        Raises:
            Exception: If an error occurs during the update process.
        """
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
        """
        Delete a blog from the database.

        Args:
            blog (Blog): The Blog object to delete.

        Returns:
            Blog: The deleted Blog object (for reference).

        Raises:
            Exception: If an error occurs during deletion.
        """
        try:
            self.db.delete(blog)
            self.db.commit()
            logger.info(f"Blog deleted successfully: {blog.id}")
            return blog
        except Exception as e:
            self.db.rollback()
            logger.exception(f"Error deleting blog {blog.id}: {e}")
            raise
