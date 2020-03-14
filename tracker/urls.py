from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('numbers/', views.get_all_numbers, name="get_all_numbers"),
    path('number/', views.track_or_increment, name="track_or_increment"),
    path('number/<int:number>', views.delete, name="delete"),
]