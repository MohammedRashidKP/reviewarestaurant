from __future__ import unicode_literals

from django.db import models

class RestaurantReview(models.Model):
	user = models.CharField(max_length=100)
	restaurantId = models.CharField(max_length=100)
	review = models.TextField()
	rating = models.IntegerField()

	def __str__(self):
		return self.name
