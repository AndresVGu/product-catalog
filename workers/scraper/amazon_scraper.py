from playwright.sync_api import sync_playwright
import re
from urllib.parse import urljoin
from core.normalizer.product_normalizer import ProductNormalizer

class AmazonScraper:
    @staticmethod
    def price_from_item(item):
        price_text = item.query_selector(".a-price .a-offscreen")

        if price_text:
            return price_text.inner_text().strip()

        price_whole = item.query_selector(".a-price-whole")
        price_fraction = item.query_selector(".a-price-fraction")

        if not price_whole:
            return None

        whole = price_whole.inner_text().replace(",", "").strip()
        fraction = price_fraction.inner_text().strip() if price_fraction else "00"

        return f"{whole}.{fraction}"

    @staticmethod
    def product_url_from_item(item):
        links = item.query_selector_all("a[href]")

        for link in links:
            href = link.get_attribute("href")

            if href and ("/dp/" in href or "/gp/product/" in href):
                absolute_url = urljoin("https://www.amazon.ca", href)
                asin_match = re.search(r"/(?:dp|gp/product)/([A-Z0-9]{10})", absolute_url)

                if asin_match:
                    return f"https://www.amazon.ca/dp/{asin_match.group(1)}"

                return absolute_url[:500]

        return None

    def search(self, query: str, limit: int = 5):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            url = f"https://www.amazon.ca/s?k={query}"
            page.goto(url, timeout=60000)

            page.wait_for_timeout(2000)

            items = page.query_selector_all("[data-component-type='s-search-result']")

            if not items:
                print(f"Amazon page title: {page.title()}")
                print(f"Amazon page url: {page.url}")
                page.screenshot(path="amazon_debug.png", full_page=True)

                with open("amazon_debug.html", "w", encoding="utf-8") as debug_file:
                    debug_file.write(page.content())

                print("Saved amazon_debug.png and amazon_debug.html")

            results = []

            for item in items[:limit]:
                title = item.query_selector("h2 span")

                raw = {
                    "title": title.inner_text() if title else None,
                    "price": self.price_from_item(item),
                    "url": self.product_url_from_item(item)
                }

                results.append(
                    ProductNormalizer.normalize_product(
                        raw,
                        source="amazon",
                        query=query
                    )
                )

            browser.close()
            return results
