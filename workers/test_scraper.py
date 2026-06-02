from workers.scraper.amazon_scraper import AmazonScraper

scraper = AmazonScraper()

results = scraper.search("laptop")

for r in results:
    print(r)