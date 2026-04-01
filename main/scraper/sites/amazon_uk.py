"""Amazon UK scraper – amazon.co.uk search results."""

from urllib.parse import quote_plus

from ..base import BaseScraper, ProductResult
from ..parser import make_soup, text, attr, extract_price, absolute_url


class AmazonUKScraper(BaseScraper):
    name = "Amazon UK"
    site_key = "amazon_uk"
    base_url = "https://www.amazon.co.uk"

    def build_search_url(self, query: str) -> str:
        return f"{self.base_url}/s?k={quote_plus(query)}"

    def parse_products(self, html: str) -> list[ProductResult]:
        soup = make_soup(html)
        sel = self.selectors
        items = soup.select(sel["product_container"])
        products: list[ProductResult] = []
        for item in items:
            title_text = text(item, sel["title"])
            if not title_text:
                continue

            # Price: try whole + fraction first, fall back to offscreen
            whole = text(item, sel["price_whole"]).replace(",", "").rstrip(".")
            fraction = text(item, sel["price_fraction"])
            if whole:
                raw_price = f"{whole}.{fraction}" if fraction else whole
            else:
                raw_price = text(item, sel["price_fallback"])
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
