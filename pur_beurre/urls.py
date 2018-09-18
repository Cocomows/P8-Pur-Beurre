from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path('', views.index, name='pur-beurre-index'),
    path('results', views.results, name='pur-beurre-results'),
    path('substitutes', views.substitutes, name='pur-beurre-subsitutes'),
    path('food', views.food, name='pur-beurre-food'),
    path('legal', views.legal, name='pur-beurre-legal'),
    path('save', views.save_product, name='pur-beurre-save'),
    path('saved', login_required(views.UserSavedProductsList.as_view()), name='saved-products')
]
