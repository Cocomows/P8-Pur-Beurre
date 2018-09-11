
import requests, json, math
from django.shortcuts import render


def index(request):
    return render(request, "pur_beurre/pages/home.html")


def results(request):

    if request.GET.get('page'):
        page = int(request.GET.get('page'))
    else:
        page = 1
    page_size = 6

    query = request.GET.get('q')

    api_url = 'https://fr.openfoodfacts.org/cgi/search.pl'
    payload = {'search_simple': 1,
               'action': 'process',
               'json': 1,
               'page_size': page_size,
               'search_terms': query,
               'page': page,
               # 'sort_by': 'nutrition_grades',

               }

    resp = requests.get(api_url, params=payload)
    food_json = json.loads(resp.text)

    nb_pages = int(math.ceil(food_json["count"] / int(food_json["page_size"])))
    api_total_url = resp.url
    return render(request, "pur_beurre/pages/results.html", locals())


def food(request):
    code = request.GET.get('code')
    api_url = "https://fr.openfoodfacts.org/api/v0/produit/"+str(code)+".json"
    resp = requests.get(api_url)
    food_json = json.loads(resp.text)

    return render(request, "pur_beurre/pages/food.html", locals())


def legal(request):
    return render(request, "pur_beurre/pages/legal.html")
