from sqlalchemy.orm import Session
from database.models import Product, ProductStore, Price
from decimal import Decimal

class PricePipeline:

    def __init__(self, db: Session):
        self.db = db

    #1. PRODUCT RESOLUTION
    def get_or_create_product(self, title: str):
        product = (
            self.db.query(Product)
            .filter(Product.name == title)
            .first()
        )

        if product:
            return product
        
        product = Product(name=title)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)

        return product
    
    #2. PRODUCT STORE RESOLUTION
    def get_or_create_product_store(
        self,
        product_id,
        store_id:int,
        url: str,
        store_sku: str | None = None,
    ):
        ps = (
            self.db.query(ProductStore)
            .filter(
                ProductStore.product_id == product_id,
                ProductStore.store_id == store_id
            )
            .first()
        )

        if ps:
            return ps

        if not url:
            raise ValueError("ProductStore requires a non-empty url")
        
        ps = ProductStore(
            product_id=product_id,
            store_id=store_id,
            store_sku=store_sku,
            url=url
        )

        self.db.add(ps)
        self.db.commit()
        self.db.refresh(ps)

        return ps
    
    #3. PRICE INSERT (HISTORICAL)
    def insert_price(self, product_store_id:  int, price: float, currency: str = "CAD"):
        price_row = Price(
            product_store_id = product_store_id,
            amount=Decimal(str(price)),
            currency=currency
        )

        self.db.add(price_row)
        self.db.commit()

        return price_row
    
    #4. FULL PIPELINE
    def run(self, product: dict, store_id: int):
        if not product.get("url"):
            raise ValueError(f"Product has no url: {product.get('title')}")

        if product.get("price") is None:
            raise ValueError(f"Product has no price: {product.get('title')}")

        product_obj = self.get_or_create_product(product["title"])

        ps = self.get_or_create_product_store(
            product_obj.id,
            store_id,
            product.get("url"),
            product.get("store_sku")
        )

        self.insert_price(
            ps.id,
            product["price"],
            product.get("currency", "CAD")
        )

        
