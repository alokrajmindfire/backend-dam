from fastapi import FastAPI
from app.config.dbconf import SessionLocal
app = FastAPI(title="User CRUD API")
# app.include_router(user_routes.router)

@app.get("/")
def root():
    db = SessionLocal()
    print("db",db.connection)
    return {"message": "User CRUD API is running!"}
