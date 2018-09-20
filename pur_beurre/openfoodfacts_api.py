import requests
import json


def get_better_products(food_json):
    """
    This function requests json of products on openfoodfacts for a given category
    and returns a list of data
    """

    relevant_category = get_relevant_category(food_json)

    better_products = []
    nutriscores_list = ['A', 'B', 'C', 'D', 'E']
    nb_products_max = 6

    # nb_product_max incremented by 1 in search in case of searched product being in the results
    api_search_url = 'https://fr-en.openfoodfacts.org/cgi/search.pl'
    payload = {'search_simple': 1,
               'action': 'process',
               'json': 1,
               'page_size': nb_products_max+1,
               'page': 1,
               'tagtype_0': 'categories',
               'tag_contains_0': 'contains',
               'tag_0': relevant_category,
               'tagtype_1': 'nutrition_grades',
               'tag_contains_1': 'contains',
               'tag_1': nutriscores_list[0],
               }

    try:
        lowest_acceptable_score = food_json['product']['nutrition_grades'].upper()

        for score_index, score in enumerate(nutriscores_list):
            if score_index <= nutriscores_list.index(lowest_acceptable_score):
                if len(better_products) < nb_products_max:
                    payload['tag_1'] = nutriscores_list[score_index]
                    search_json = requests.get(api_search_url, params=payload).json()

                    for product in search_json['products']:
                        if len(better_products) < nb_products_max:
                            if food_json['product']['code'] != product['code']:
                                better_products.append(product)

                        else:
                            return better_products

                else:
                    return better_products
            else:
                return better_products

        return better_products
    except KeyError:
        better_products.append("Unknown Score")
    return better_products


def get_relevant_category(food_json):
    # We get the relevant product category which is the last in the hierarchy list (fewer products)

    try:
        relevant_category = food_json["product"]["categories_hierarchy"][-1]
        # handling the case where there is only 1 product in the category :
        category_json = requests.get("https://fr-en.openfoodfacts.org/category/" + relevant_category + ".json").json()
        if category_json['count'] == 1:
            relevant_category = food_json["product"]["categories_hierarchy"][-2]

    except KeyError:
        relevant_category = "Unknown category"

    return relevant_category

