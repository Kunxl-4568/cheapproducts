"""
selectors.py – centralised CSS selector definitions for every supported site.

Each site registers a dict of selectors used by the corresponding parser.
Adding a new site = adding one new key here + one site scraper module.
"""

SELECTORS: dict[str, dict[str, str]] = {
    # ------------------------------------------------------------------
    # Amazon UK
    # ------------------------------------------------------------------
    "amazon_uk": {
        "product_container": 'div[data-component-type="s-search-result"]',
        "title": "h2 span",
        "price_whole": "span.a-price-whole",
        "price_fraction": "span.a-price-fraction",
        "price_fallback": "span.a-offscreen",
        "image": "img.s-image",
        "link": "a.a-link-normal",
    },
    # ------------------------------------------------------------------
    # eBay UK
    # ------------------------------------------------------------------
    "ebay_uk": {
        "product_container": "li.s-card[data-listingid]",
        "title": "div.s-card__title",
        "price": "span.s-card__price",
        "image": "img.s-card__image",
        "link": "a.s-card__link",
    },
    # ------------------------------------------------------------------
    # Etsy (UK region)
    # ------------------------------------------------------------------
    "etsy_uk": {
        "product_container": "div.wt-grid__item-xs-6",
        "title": "h3",
        "price": "span.currency-value",
        "currency_symbol": "span.currency-symbol-before",
        "image": "img.wt-width-full",
        "link": "a.listing-link",
    },
    # ------------------------------------------------------------------
    # TikTok Shop
    # ------------------------------------------------------------------
    "tiktok_shop": {
        "product_container": "div[class*='ProductCard']",
        "title": "h3",
        "price": "span[class*='price']",
        "image": "img",
        "link": "a",
    },
    # ------------------------------------------------------------------
    # Facebook Marketplace
    # ------------------------------------------------------------------
    "facebook_marketplace": {
        "product_container": "div[class*='x9f619']",
        "title": "span.x1lliihq",
        "price": "span.x193iq5w",
        "image": "img",
        "link": "a",
    },
    # ------------------------------------------------------------------
    # Wix eCommerce  (generic Wix store layout)
    # ------------------------------------------------------------------
    "wix": {
        "product_container": "li[data-hook='product-list-grid-item']",
        "title": "[data-hook='product-item-name']",
        "price": "[data-hook='product-item-price-to-pay']",
        "image": "[data-hook='product-item-images'] img",
        "link": "[data-hook='product-item-container'] a",
    },
    # ------------------------------------------------------------------
    # BigCommerce  (generic Catalyst / Cornerstone theme)
    # ------------------------------------------------------------------
    "bigcommerce": {
        "product_container": "li.product",
        "title": "h3.card-title a",
        "price": "span.price--withTax",
        "image": "img.card-image",
        "link": "h3.card-title a",
    },
}
