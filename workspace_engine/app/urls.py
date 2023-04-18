from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('app/', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('get_recommendations/', views.get_recommendations, name='get_recommendations')
]