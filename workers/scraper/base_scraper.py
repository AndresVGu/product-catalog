class BaseScraper:
    def search(self, query: str):
        raise NotImplementedError
    
    def get_price(self, url: str):
        raise NotImplementedError