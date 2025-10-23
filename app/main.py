from fastapi import FastAPI
from app.config.dbconf import SessionLocal, engine
from app.models import user_model
from sqlalchemy import text
from app.routes import user_routes

app = FastAPI(title="User CRUD API")
app.include_router(user_routes.router)

user_model.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    db = SessionLocal()
    try:
        return {"message": "User CRUD API is running!"}
    finally:
        db.close()
