from django.contrib import admin

from .models import Client, ProductArea, FeatureRequest

admin.site.register(Client)
admin.site.register(ProductArea)
admin.site.register(FeatureRequest)