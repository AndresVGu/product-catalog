from database.connection import SessionLocal
from database.models import Store, TrackingRule

db = SessionLocal()

store = db.query(Store).first()

rule = TrackingRule(
    store_id=store.id,
    search_query="laptop",
    category_hint="electronics",
    active=True
)

db.add(rule)
db.commit()

print("Tracking rule created")