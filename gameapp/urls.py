from django.urls import path
from .views import index, start_game

urlpatterns = [
    path('', index, name='index'),
    path('start_game/', start_game, name='start_game'),
]