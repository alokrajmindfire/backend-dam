from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.dbconf import SessionLocal
from app.controllers.blog_controller import BlogController
from app.schemas.blog_schema import BlogCreate, BlogUpdate, BlogResponse
from app.middleware.auth_middleware import get_current_user
from app.schemas.user_schema import UserResponse
from app.config.dbconf import get_db

router = APIRouter(prefix="/blogs", tags=["Blogs"])

@router.get("/", response_model=list[BlogResponse])
def list_blogs(db: Session = Depends(get_db),current_user: UserResponse = Depends(get_current_user)):
    """
    Retrieve a list of all blogs from the database.

    Args:
        db (Session): The SQLAlchemy session dependency for database access.

    Returns:
        list[BlogResponse]: A list of blog objects containing details such as
        title, content, author, and timestamps.

    Raises:
        HTTPException: None explicitly raised here, but may propagate from the controller.
    """
    controller = BlogController(db)
    return controller.get_blogs()

@router.get("/{blog_id}", response_model=BlogResponse)
def get_blog(blog_id: int, db: Session = Depends(get_db),current_user: UserResponse = Depends(get_current_user)):
    """
    Retrieve a specific blog by its ID.

    Args:
        blog_id (int): The unique identifier of the blog to retrieve.
        db (Session): The SQLAlchemy session dependency for database access.

    Returns:
        BlogResponse: The details of the requested blog.

    Raises:
        HTTPException: 404 error if the blog with the given ID is not found.
    """
    controller = BlogController(db)
    blog = controller.get_blog(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.post("/", response_model=BlogResponse)
def create_blog(blog_create: BlogCreate, db: Session = Depends(get_db),current_user: UserResponse = Depends(get_current_user)):
    """
    Create a new blog entry in the database.

    Args:
        blog_create (BlogCreate): A schema object containing the new blog's title,
                                 content, author, and other required fields.
        db (Session): The SQLAlchemy session dependency for database access.

    Returns:
        BlogResponse: The details of the newly created blog.
    """
    controller = BlogController(db)
    blog_data = blog_create.model_dump()
    blog_data["author_id"] = current_user.id

    return controller.create_blog(BlogCreate(**blog_data),author_id=current_user.id)

@router.put("/{blog_id}", response_model=BlogResponse)
def update_blog(blog_id: int, blog_update: BlogUpdate, db: Session = Depends(get_db),current_user: UserResponse = Depends(get_current_user)):
    """
    Update an existing blog post with new data.

    Args:
        blog_id (int): The unique identifier of the blog to update.
        blog_update (BlogUpdate): A schema object containing updated blog fields.
        db (Session): The SQLAlchemy session dependency for database access.

    Returns:
        BlogResponse: The updated blog details.

    Raises:
        HTTPException: 404 error if the specified blog does not exist.
    """
    controller = BlogController(db)
    blog = controller.update_blog(blog_id, blog_update)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.delete("/{blog_id}", response_model=BlogResponse)
def delete_blog(blog_id: int, db: Session = Depends(get_db),current_user: UserResponse = Depends(get_current_user)):
    """
    Delete a blog entry from the database.

    Args:
        blog_id (int): The unique identifier of the blog to delete.
        db (Session): The SQLAlchemy session dependency for database access.

    Returns:
        BlogResponse: The details of the deleted blog.

    Raises:
        HTTPException: 404 error if the specified blog does not exist.
    """
    controller = BlogController(db)
    blog = controller.delete_blog(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog
