from django.db import models


class Product(models.Model):
	title = models.CharField(max_length=500)
	price = models.DecimalField(max_digits=12, decimal_places=2)
	image_url = models.URLField(blank=True, null=True)
	source_url = models.URLField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	source = models.CharField(max_length=200, blank=True, null=True)
	fetched_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.title} — {self.source} — {self.price}"
