import logging
import requests, json, math
from django.shortcuts import render, get_object_or_404
from .models import Product, Save
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DeleteView
from django.db import IntegrityError
from .openfoodfacts_api import get_better_products


#Get an instance of a logger 
logger = logging.getLogger(__name__)

class UserSavedProductsList(ListView):
    model = Save
    template_name = 'pur_beurre/pages/saved_products.html'
    context_object_name = 'saves'
    paginate_by = 6
    ordering = ['-date']

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return Save.objects.filter(saved_by=user).order_by('-date')


def index(request):
    return render(request, "pur_beurre/pages/home.html")
	

def results(request):

    if request.GET.get('page'):
        page = int(request.GET.get('page'))
    else:
        page = 1
    page_size = 6

    query = request.GET.get('q')

    api_url = 'https://fr-en.openfoodfacts.org/cgi/search.pl'
    payload = {'search_simple': 1,
               'action': 'process',
               'json': 1,
               'page_size': page_size,
               'search_terms': query,
               'page': page,
               }

    resp = requests.get(api_url, params=payload)
    food_json = json.loads(resp.text)

    nb_pages = int(math.ceil(food_json["count"] / int(food_json["page_size"])))
    api_total_url = resp.url
    logger.info('New search', exc_info=True, extra={'search term:': query})
    return render(request, "pur_beurre/pages/results.html", locals())


def substitutes(request):

    if request.GET.get('page'):
        page = int(request.GET.get('page'))
    else:
        page = 1
    page_size = 6

    # Information to keep for locals : json about the selected product
    # and list of json about each better product

    code = request.GET.get('code')
    # We get the product info from the product code
    api_product_url = "https://fr-en.openfoodfacts.org/api/v0/produit/"+str(code)+".json"
    food_json = requests.get(api_product_url).json()

    # nb_pages = int(math.ceil(food_json["count"] / int(food_json["page_size"])))
    better_products = get_better_products(food_json)
    # print(better_products)
    return render(request, "pur_beurre/pages/substitutes.html", locals())


def food(request):
    code = request.GET.get('code')
    # We get the product info from the product code
    api_product_url = "https://fr-en.openfoodfacts.org/api/v0/produit/"+str(code)+".json"
    food_json = requests.get(api_product_url).json()
    return render(request, "pur_beurre/pages/food.html", locals())


def legal(request):
    return render(request, "pur_beurre/pages/legal.html")


@login_required
def save_product(request):

    code = request.GET.get('code')
    # We get the product info from the product code
    api_product_url = "https://fr-en.openfoodfacts.org/api/v0/produit/"+str(code)+".json"
    food_json = requests.get(api_product_url).json()

    # save product
    list_scores = ['N/A', 'A', 'B', 'C', 'D', 'E']

    nutriscore_int = list_scores.index(food_json['product']['nutrition_grades'].upper())

    product_to_save = Product(name=food_json['product']['product_name'], brand=food_json['product']['brands'],
                              code=food_json['product']['code'], nutriscore=nutriscore_int,
                              description=food_json['product']['ingredients_text'],
                              image=food_json['product']['image_url'],
                              link_openfoodfacts="https://fr.openfoodfacts.org/produit/"+food_json['product']['code'],)

    product_to_save.save()

    try:
        save = Save(saved_by=request.user, saved_product=product_to_save)
        save.save()
    except IntegrityError as error:
        print(error)
        message_already_saved = "Vous avez déjà enregistré ce produit précédemment, " \
                                "il n'a pas été rajouté à votre liste de produits sauvegardés."

    return render(request, "pur_beurre/pages/save.html", locals())


class SaveDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Save
    template_name = 'pur_beurre/pages/save_confirm_delete.html'
    success_url = '/saved'

    def test_func(self):
        save = self.get_object()
        if self.request.user == save.saved_by:
            return True
        return False


 def handler404(request):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)
