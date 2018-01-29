from django.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    path('', views.FeatureHome.as_view(), name='featurehome'),
	path('requests', views.FeatureList.as_view(), name='features'),
	url('addrequest', views.AddRequest.as_view()),
]