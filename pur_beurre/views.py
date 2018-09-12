
import requests, json, math
from django.shortcuts import render


NUTRISCORE = {
    0: 'N/A',
    1: 'A',
    2: 'B',
    3: 'C',
    4: 'D',
    5: 'E'
}


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
    return render(request, "pur_beurre/pages/results.html", locals())


def food(request):

    # Information to keep for locals : json about the selected product
    # and list of json about each better product

    code = request.GET.get('code')
    # We get the product info from the product code
    api_product_url = "https://fr-en.openfoodfacts.org/api/v0/produit/"+str(code)+".json"
    food_json = requests.get(api_product_url).json()

    # relevant_category = get_relevant_category(food_json)
    #
    # api_search_url = 'https://fr-en.openfoodfacts.org/cgi/search.pl'
    # payload = {'search_simple': 1,
    #            'action': 'process',
    #            'json': 1,
    #            'page_size': 10,
    #            'page': 1,
    #            'tagtype_0': 'categories',
    #            'tag_contains_0': 'contains',
    #            'tag_0': relevant_category,
    #            'tagtype_1': 'nutrition_grades',
    #            'tag_contains_1': 'contains',
    #            'tag_1': 'A',
    #            }
    #
    # resp = requests.get(api_search_url, params=payload)
    # search_json_url = resp.url
    # products_a = get_number_products(relevant_category, 'A')
    # products_b = get_number_products(relevant_category, 'B')
    # products_c = get_number_products(relevant_category, 'C')
    # products_d = get_number_products(relevant_category, 'D')
    # products_e = get_number_products(relevant_category, 'E')
    #
    # url_a = get_url_search(relevant_category, 'A')
    # url_b = get_url_search(relevant_category, 'B')
    # url_c = get_url_search(relevant_category, 'C')
    # url_d = get_url_search(relevant_category, 'D')
    # url_e = get_url_search(relevant_category, 'E')
    # print(get_better_products(food_json))
    better_products = get_better_products(food_json)
    return render(request, "pur_beurre/pages/food.html", locals())


def legal(request):
    return render(request, "pur_beurre/pages/legal.html")


def get_url_search(category, grade):
    api_search_url = 'https://fr-en.openfoodfacts.org/cgi/search.pl'
    payload = {'search_simple': 1,
               'action': 'process',
               'json': 1,
               'page_size': 10,
               'page': 1,
               'tagtype_0': 'categories',
               'tag_contains_0': 'contains',
               'tag_0': category,
               'tagtype_1': 'nutrition_grades',
               'tag_contains_1': 'contains',
               'tag_1': grade,
               }

    return requests.get(api_search_url, params=payload).url


def get_number_products(category, grade):
    api_search_url = 'https://fr-en.openfoodfacts.org/cgi/search.pl'
    payload = {'search_simple': 1,
               'action': 'process',
               'json': 1,
               'page_size': 10,
               'page': 1,
               'tagtype_0': 'categories',
               'tag_contains_0': 'contains',
               'tag_0': category,
               'tagtype_1': 'nutrition_grades',
               'tag_contains_1': 'contains',
               'tag_1': grade,
               }

    search_json = requests.get(api_search_url, params=payload).json()
    return search_json['count']


def get_better_products(food_json):
    """
    This function requests json of products on openfoodfacts for a given category
    and returns a list of data
    """

    relevant_category = get_relevant_category(food_json)

    better_products = []
    nutriscores_list = ['A', 'B', 'C', 'D', 'E']
    nb_products_max = 9
    api_search_url = 'https://fr-en.openfoodfacts.org/cgi/search.pl'
    payload = {'search_simple': 1,
               'action': 'process',
               'json': 1,
               'page_size': nb_products_max,
               'page': 1,
               'tagtype_0': 'categories',
               'tag_contains_0': 'contains',
               'tag_0': relevant_category,
               'tagtype_1': 'nutrition_grades',
               'tag_contains_1': 'contains',
               'tag_1': nutriscores_list[0],
               }

    lowest_acceptable_score = food_json['product']['nutrition_grades'].upper()
    print("lowest acceptable score: "+str(lowest_acceptable_score))

    for score_index, score in enumerate(nutriscores_list):
        if score_index <= nutriscores_list.index(lowest_acceptable_score):
            if len(better_products) < nb_products_max:

                print(str(score_index)+" : "+score)
                payload['tag_1'] = nutriscores_list[score_index]
                search_json = requests.get(api_search_url, params=payload).json()
                print(requests.get(api_search_url, params=payload).url)

                for product in search_json['products']:
                    if len(better_products) < nb_products_max:
                        better_products.append(product['product_name'])
                    else:
                        return better_products

            else:
                return better_products
        else:
            return better_products

    return better_products


def get_relevant_category(food_json):
    # We get the relevant product category which is the last in the hierarchy list (fewer products)
    relevant_category = food_json["product"]["categories_hierarchy"][-1]

    # handling the case where there is only 1 product in the category :
    category_json = requests.get("https://fr-en.openfoodfacts.org/category/" + relevant_category + ".json").json()
    if category_json['count'] == 1:
        relevant_category = food_json["product"]["categories_hierarchy"][-2]
    return relevant_category
