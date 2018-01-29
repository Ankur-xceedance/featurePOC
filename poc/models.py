from django.db import models
from datetime import datetime


class Client(models.Model):
	#Master model for client data
	client = models.CharField(max_length=200)
	
	def __str__(self):
		return self.client
	
class ProductArea(models.Model):
	#Master model for product data
	product = models.CharField(max_length=200)
	
	def __str__(self):
		return self.product
		
class FeatureRequest(models.Model):
	#model containing feature request data
	STATUS_CHOICES = (
		('0', 'Created'),
		('1', 'In Progress'),
		('2', 'Completed'),
		('3', 'Rejected'),
	)
	title = models.CharField(max_length=200)
	desc = models.TextField()
	product_area = models.ForeignKey(ProductArea, on_delete=models.CASCADE)
	client = models.ForeignKey(Client,  on_delete=models.CASCADE)
	priority = models.IntegerField(default=0)
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=0)
	target_date = models.DateField()
	create_date = models.DateTimeField(default=datetime.now())
	
	def __str__(self):
		return self.title
	