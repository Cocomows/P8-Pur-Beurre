import os
import requests
import json
import django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "P8_Pur_Beurre.settings"
)
django.setup()
# Now this script or any imported module can use any part of Django it needs.
from pur_beurre.models import Product


for product in Product.objects.all():
    # We get the product info from the product code and we update the current product
    code = product.code
    api_product_url = "https://fr-en.openfoodfacts.org/api/v0/produit/" + str(code) + ".json"
    food_json = requests.get(api_product_url).json()
    list_scores = ['N/A', 'A', 'B', 'C', 'D', 'E']
    nutriscore_int = list_scores.index(food_json['product']['nutrition_grades'].upper())
    product = Product(name=food_json['product']['product_name'], brand=food_json['product']['brands'],
                      code=food_json['product']['code'], nutriscore=nutriscore_int,
                      description=food_json['product']['ingredients_text'],
                      image=food_json['product']['image_url'],
                      link_openfoodfacts="https://fr.openfoodfacts.org/produit/" + food_json['product']['code'], )
    product.save()
