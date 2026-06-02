from database.connection import engine
from database.models.base import Base

#All models
import database.models.category
import database.models.price
import database.models.product
import database.models.product_store
import database.models.store
import database.models.tracking_rule

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully")


if __name__ == "__main__":
    create_tables()