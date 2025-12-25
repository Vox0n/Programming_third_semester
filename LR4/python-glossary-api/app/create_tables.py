import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine
import models

print("Creating database tables...")
models.Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
