"""
Wix eCommerce scraper.

Wix is a website-builder platform – there is no single centralised search
URL.  This scraper targets a *specific* Wix store.  Set ``store_url`` on the
instance (or subclass) to point at a particular Wix-powered shop.

By default the scraper is a no-op (returns []) until a store URL is configured.
"""

from urllib.parse import quote_plus

from ..base import BaseScraper, ProductResult
from ..parser import make_soup, text, attr, extract_price, absolute_url


class WixScraper(BaseScraper):
    name = "Wix Store"
    site_key = "wix"
    base_url = ""  # must be set to a real Wix store URL

    def build_search_url(self, query: str) -> str:
        if not self.base_url:
            return ""
        return f"{self.base_url}/product-page?search={quote_plus(query)}"

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
