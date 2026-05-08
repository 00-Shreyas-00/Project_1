from app.services.db_service import engine, Base
from app.models.user import UserDB

def init_db():
    print("Creating tables in the database...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
