import os

from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError

from database.connection import SessionLocal
from core.normalizer.product_normalizer import ProductNormalizer
from core.pipeline.price_pipeline import PricePipeline
from database.models import Store
from workers.api import EbayClient
from workers.api.ebay_client import EbayApiError
from workers.scraper.amazon_scraper import AmazonScraper

load_dotenv()


STORE_CONFIG = {
    "amazon": {
        "name": "Amazon",
        "country": "CA",
        "website": "https://www.amazon.ca",
        "source": AmazonScraper,
    },
    "ebay": {
        "name": "eBay",
        "country": "CA",
        "website": "https://www.ebay.ca",
        "source": EbayClient,
    },
}


def get_or_create_store(db, source_name: str):
    config = STORE_CONFIG[source_name]
    store = db.query(Store).filter(Store.name == config["name"]).first()

    if store:
        return store

    store = Store(
        name=config["name"],
        country=config["country"],
        website=config["website"],
    )
    db.add(store)
    db.commit()
    db.refresh(store)

    return store


def build_source(source_name: str):
    if source_name not in STORE_CONFIG:
        available_sources = ", ".join(STORE_CONFIG)
        raise ValueError(f"Unknown source '{source_name}'. Use one of: {available_sources}")

    return STORE_CONFIG[source_name]["source"]()

def run():
    source_name = os.getenv("PRICE_SOURCE", "amazon").lower()
    search_query = os.getenv("PRICE_QUERY", "ram")
    search_limit = int(os.getenv("PRICE_LIMIT", "5"))

    try:
        source = build_source(source_name)
    except (ValueError, EbayApiError) as error:
        print(f"Runner stopped: {error}")
        return

    db = SessionLocal()

    try:
        store = get_or_create_store(db, source_name)
        pipeline = PricePipeline(db)
        raw_products = source.search(search_query, limit=search_limit)
        print(f"Source: {source_name}")
        print(f"Query: {search_query}")
        print(f"Found {len(raw_products)} products")

        for raw in raw_products:
            normalized = ProductNormalizer.normalize_product(raw)

            try:
                pipeline.run(
                    normalized,
                    store_id=store.id
                )
            except ValueError as error:
                print(f"Skipping product: {error}")
            except SQLAlchemyError as error:
                db.rollback()
                print(f"Skipping product after database error: {error}")
    except (ValueError, EbayApiError, SQLAlchemyError) as error:
        db.rollback()
        print(f"Runner stopped: {error}")
    finally:
        db.close()

if __name__ == "__main__":
    run()
