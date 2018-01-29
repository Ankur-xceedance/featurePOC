from django.contrib import admin
from django.urls import path
from poc import views
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', include('poc.urls')),
]
