"""
TikTok Shop scraper.

NOTE: TikTok Shop pages are heavily JavaScript-rendered.  With plain
requests + BeautifulSoup the HTML returned is mostly empty shell.
This scraper attempts to extract whatever the initial HTML provides;
for full coverage a headless browser or official API would be needed.
"""

from urllib.parse import quote_plus

from ..base import BaseScraper, ProductResult
from ..parser import make_soup, text, attr, extract_price, absolute_url


class TikTokShopScraper(BaseScraper):
    name = "TikTok Shop"
    site_key = "tiktok_shop"
    base_url = "https://shop.tiktok.com"

    def build_search_url(self, query: str) -> str:
        return f"{self.base_url}/search?q={quote_plus(query)}"

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
