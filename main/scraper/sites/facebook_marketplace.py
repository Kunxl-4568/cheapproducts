"""
Facebook Marketplace scraper.

NOTE: Facebook Marketplace requires authentication and is almost entirely
client-side rendered.  This scraper makes a best-effort attempt but will
likely return no results without a logged-in session cookie.  For
production use, the Facebook/Meta Commerce API is recommended.
"""

from urllib.parse import quote_plus

from ..base import BaseScraper, ProductResult
from ..parser import make_soup, text, attr, extract_price, absolute_url


class FacebookMarketplaceScraper(BaseScraper):
    name = "Facebook Marketplace"
    site_key = "facebook_marketplace"
    base_url = "https://www.facebook.com"

    def build_search_url(self, query: str) -> str:
        return (
            f"{self.base_url}/marketplace/search?"
            f"query={quote_plus(query)}"
        )

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
