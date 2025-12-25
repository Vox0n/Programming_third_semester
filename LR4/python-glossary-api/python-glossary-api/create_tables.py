from database import engine
from models import Base

def create_tables():
    """Создает все таблицы в базе данных"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")