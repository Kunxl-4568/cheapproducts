"""
storage.py – Persist scraped results into the Django Product model.

This is optional – results can be shown directly from memory.
Call ``save_results`` when you want to cache products in the DB.
"""

import logging

logger = logging.getLogger(__name__)


def save_results(products: list[dict]) -> int:
    """
    Bulk-create Product rows from a list of scraper result dicts.
    Returns the number of rows created.

    Import is deferred so that this module can be loaded without Django
    being fully initialised (e.g. during tests).
    """
    from main.models import Product  # late import for Django readiness

    objs = []
    for p in products:
        if not p.get("title"):
            continue
        objs.append(
            Product(
                title=p["title"],
                price=p.get("price") or 0,
                image_url=p.get("image", ""),
                source_url=p.get("url", ""),
                description=p.get("description", ""),
                source=p.get("source", ""),
            )
        )
    if objs:
        created = Product.objects.bulk_create(objs)
        logger.info("Saved %d products to DB", len(created))
        return len(created)
    return 0
