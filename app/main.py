from fastapi import FastAPI
from app.config.dbconf import SessionLocal, engine
from app.models import user_model
from sqlalchemy import text

app = FastAPI(title="User CRUD API")

user_model.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT 1")).scalar()
        print("DB connected, test query result:", result)
        return {"message": "User CRUD API is running!"}
    finally:
        db.close()
