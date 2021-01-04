from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new_search', views.new_search, name='new_search'),
    path('generate_movie/', views.random_movie, name='generate_movie'),
]
