from django.shortcuts import render
from django.http import HttpResponse

from . import scrapers
from .models import Product


def home(request):
    return HttpResponse("Hello from Django!")


def search_view(request):
    q = request.GET.get('q', '').strip()
    results = []
    if q:
        # Prefer DB-backed demo products if any exist for the query.
        qs = Product.objects.filter(title__icontains=q)
        if qs.exists():
            results = []
            for p in qs.order_by('price'):
                results.append({
                    'title': p.title,
                    'price': p.price,
                    'image': p.image_url,
                    'url': p.source_url,
                    'description': p.description,
                    'source': p.source,
                })
        else:
            results = scrapers.search_products(q)
    return render(request, 'main/search.html', {'query': q, 'results': results})