from django.core.management.base import BaseCommand
from main.models import Product


def demo_products():
    return [
        {
            'title': 'Budget Laptop 14" - Model A',
            'price': '299.99',
            'image_url': 'https://via.placeholder.com/200x150?text=Budget+Laptop+A',
            'source_url': 'https://example.com/product/budget-a',
            'description': 'Lightweight 14 inch laptop, 4GB RAM, 128GB SSD',
            'source': 'DemoStore'
        },
        {
            'title': 'Midrange Laptop 15" - Model B',
            'price': '599.00',
            'image_url': 'https://via.placeholder.com/200x150?text=Midrange+Laptop+B',
            'source_url': 'https://example.com/product/mid-b',
            'description': '15 inch laptop, 8GB RAM, 256GB SSD',
            'source': 'DemoStore'
        },
        {
            'title': 'Premium Laptop 16" - Model C',
            'price': '1299.50',
            'image_url': 'https://via.placeholder.com/200x150?text=Premium+Laptop+C',
            'source_url': 'https://example.com/product/premium-c',
            'description': '16 inch laptop, 16GB RAM, 1TB SSD',
            'source': 'DemoStore'
        },
        {
            'title': 'Refurb Laptop 14" - Model D',
            'price': '199.00',
            'image_url': 'https://via.placeholder.com/200x150?text=Refurb+Laptop+D',
            'source_url': 'https://example.com/product/refurb-d',
            'description': 'Refurbished 14 inch laptop, 4GB RAM, 64GB eMMC',
            'source': 'DemoStore'
        }
    ]


class Command(BaseCommand):
    help = 'Seed demo Product rows for local testing'

    def handle(self, *args, **options):
        items = demo_products()
        created = 0
        for it in items:
            p, ok = Product.objects.get_or_create(
                title=it['title'],
                defaults={
                    'price': it['price'],
                    'image_url': it['image_url'],
                    'source_url': it['source_url'],
                    'description': it['description'],
                    'source': it['source'],
                }
            )
            if ok:
                created += 1
        self.stdout.write(self.style.SUCCESS(f'Seeded {created} demo products'))
