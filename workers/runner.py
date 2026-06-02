from database.connection import SessionLocal
from database.models import TrackingRule, ProductStore, Price
from decimal import Decimal

def run_scraper():
    db = SessionLocal()

    rules = db.query(TrackingRule).filter(TrackingRule.active == True).all()

    for rule in rules:
        print(f"Scraping: {rule.search_query}")

        #later we connect with the real scrapre
        price_value = 199.99

        ps = db.query(ProductStore).first()

        price = Price(
            product_store_id=ps.id,
            amount=Decimal(price_value),
            currency="CAD"
        )

        db.add(price)
        db.commit()

    db.close()

if __name__ == "__main__":
    run_scraper()