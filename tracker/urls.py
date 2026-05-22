# tracker/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('',           views.dashboard,   name='dashboard'),
    path('food-log/',  views.food_log,    name='food_log'),
    path('my-plan/',   views.my_plan,     name='my_plan'),
]