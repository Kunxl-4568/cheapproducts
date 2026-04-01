"""eBay UK scraper – ebay.co.uk search results."""

from urllib.parse import quote_plus

from ..base import BaseScraper, ProductResult
from ..parser import make_soup, text, attr, extract_price, absolute_url


class EbayUKScraper(BaseScraper):
    name = "eBay UK"
    site_key = "ebay_uk"
    base_url = "https://www.ebay.co.uk"

    def build_search_url(self, query: str) -> str:
        return f"{self.base_url}/sch/i.html?_nkw={quote_plus(query)}"

    def parse_products(self, html: str) -> list[ProductResult]:
        soup = make_soup(html)
        sel = self.selectors
        items = soup.select(sel["product_container"])
        products: list[ProductResult] = []
        for item in items:
            title_text = text(item, sel["title"])
            # Skip eBay placeholder card and empty titles
            if not title_text or title_text.lower().startswith("shop on ebay"):
                continue

            raw_price = text(item, sel["price"])
            price = extract_price(raw_price)

            image_url = attr(item, sel["image"], "src")
            # Some images use data-defer-load for lazy loading
            if not image_url:
                image_url = attr(item, sel["image"], "data-defer-load")
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
