import re

class ProductNormalizer:

    @staticmethod
    def normalize_price(price_text: str):
        if not price_text:
            return None
        
        price_text = "" if price_text is None else str(price_text)

        cleaned = re.sub(r"[^0-9.]", "", price_text)

        try:
            return float(cleaned) if cleaned else None
        except:
            return None
        
    @staticmethod
    def normalize_title(title: str):
        if not title:
            return "N/A"
        return title.strip()
    
    @staticmethod
    def normalize_product(raw: dict, source: str= "amazon", query: str = None):
        return{
            "title": ProductNormalizer.normalize_title(raw.get("title")),
            "price": ProductNormalizer.normalize_price(raw.get("price")),
            "currency": raw.get("currency", "CAD"),
            "source": raw.get("source", source),
            "query": raw.get("query", query),
            "url": raw.get("url"),
            "store_sku": raw.get("store_sku")
        }
