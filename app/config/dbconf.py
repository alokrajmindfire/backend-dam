from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
SQLALCHEMY_DATABASE_URL = "postgresql://ecom:123456@localhost:5432/ecom"
print("Database URL is ",SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
