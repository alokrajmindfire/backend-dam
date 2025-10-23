from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.dbconf import SessionLocal
from app.controllers.blog_controller import BlogController
from app.schemas.blog_schema import BlogCreate, BlogUpdate, BlogResponse

router = APIRouter(prefix="/blogs", tags=["Blogs"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[BlogResponse])
def list_blogs(db: Session = Depends(get_db)):
    controller = BlogController(db)
    return controller.get_blogs()

@router.get("/{blog_id}", response_model=BlogResponse)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    controller = BlogController(db)
    blog = controller.get_blog(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.post("/", response_model=BlogResponse)
def create_blog(blog_create: BlogCreate, db: Session = Depends(get_db)):
    controller = BlogController(db)
    return controller.create_blog(blog_create)

@router.put("/{blog_id}", response_model=BlogResponse)
def update_blog(blog_id: int, blog_update: BlogUpdate, db: Session = Depends(get_db)):
    controller = BlogController(db)
    blog = controller.update_blog(blog_id, blog_update)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.delete("/{blog_id}", response_model=BlogResponse)
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    controller = BlogController(db)
    blog = controller.delete_blog(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog
