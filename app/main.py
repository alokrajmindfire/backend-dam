from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.dbconf import SessionLocal, engine
from app.routes import user_routes, blog_route
from app.models import Base


app = FastAPI(title="User CRUD API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
)
Base.metadata.create_all(bind=engine)

app.include_router(user_routes.router)
app.include_router(blog_route.router)

@app.get("/")
def root():
    db = SessionLocal()
    try:
        return {"message": "User CRUD API is running!"}
    finally:
        db.close()
