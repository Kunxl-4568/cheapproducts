"""
BigCommerce scraper.

BigCommerce is a hosted e-commerce platform – there is no single search
endpoint.  This scraper targets a *specific* BigCommerce-powered store.
Set ``store_url`` on the instance (or subclass) to point at a shop, e.g.
``https://store.example.com``.

By default the scraper is a no-op (returns []) until a store URL is configured.
"""

from urllib.parse import quote_plus

from ..base import BaseScraper, ProductResult
from ..parser import make_soup, text, attr, extract_price, absolute_url


class BigCommerceScraper(BaseScraper):
    name = "BigCommerce"
    site_key = "bigcommerce"
    base_url = ""  # must be set to a real BigCommerce store URL

    def build_search_url(self, query: str) -> str:
        if not self.base_url:
            return ""
        return f"{self.base_url}/search.php?search_query={quote_plus(query)}"

    def search(self, query: str) -> list[dict]:
        if not self.base_url:
            return []
        return super().search(query)

    def parse_products(self, html: str) -> list[ProductResult]:
        soup = make_soup(html)
        sel = self.selectors
        items = soup.select(sel["product_container"])
        products: list[ProductResult] = []
        for item in items:
            title_text = text(item, sel["title"])
            if not title_text:
                continue

            raw_price = text(item, sel["price"])
            price = extract_price(raw_price)

            image_url = attr(item, sel["image"], "src")
            href = attr(item, sel["link"], "href")
            link = absolute_url(href, self.base_url)

            products.append(
                ProductResult(
                    title=title_text,
                    price=price,
                    image=image_url,
                    url=link,
                    source=self.name,
                )
            )
        return products
