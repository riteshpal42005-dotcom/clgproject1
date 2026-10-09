from core.database import Base, engine
from models import Businesses, Products, Sales, SaleItems

print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")
