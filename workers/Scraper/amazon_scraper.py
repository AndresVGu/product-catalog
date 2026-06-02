import random

class AmazonScraper:
    def search(self, query : str):
        return[{
            "title": query,
            "url": "https://amazon.ca/example",
            "price": round(random.uniform(10, 500), 2)
        }]