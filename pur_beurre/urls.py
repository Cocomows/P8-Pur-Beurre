from django.urls import path

from . import views


app_name = 'pur_beurre'

urlpatterns = [
    path('', views.index, name='index'),
    path('results', views.results, name='results'),
    path('user', views.user, name='user'),
    path('food', views.food, name='food'),
    path('legal', views.legal, name='legal'),
]