from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='pur-beurre-index'),
    path('results', views.results, name='pur-beurre-results'),
    path('food', views.food, name='pur-beurre-food'),
    path('legal', views.legal, name='pur-beurre-legal'),

]
