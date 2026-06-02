from database.connection import SessionLocal
from database.models import Category,Product, Store, ProductStore

db = SessionLocal()

#Store
store = Store(name="Rugged Books", country="CA")

# category
category = Category(name="laptop")



db.add(store)
db.add(category)
db.commit()

db.refresh(store)
db.refresh(category)

# Product
product = Product(
    name = "CF-33 Toughbook",
    brand = "Panasonic",
    category_id = category.id
)

db.add(product)
db.commit()
db.refresh(product)

#ProductStore
product_store = ProductStore(
    product_id = product.id,
    store_id=store.id,
    store_sku="LE-34VM",
    url="https://example.com"
)

db.add(product_store)
db.commit()

print("✅  Seed Completed")