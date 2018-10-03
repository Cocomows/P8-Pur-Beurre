import json
from django.test import TestCase
from pur_beurre.openfoodfacts_api import get_relevant_category, get_better_products


class TestsAPI(TestCase):

    def setUp(self):
        self.mock_json = '{"product":{"categories_hierarchy":["en:breakfasts","en:spreads","en:sweet-spreads",' \
            '"fr:pates-a-tartiner","en:chocolate-spreads","en:hazelnut-spreads","en:cocoa-and-hazelnuts-spreads"],' \
            '"nutrition_grades":"e","code":"3017620429484"}}'
        self.food_json = json.loads(self.mock_json)

    def test_get_relevant_category(self):
        """
        Test the get_relevant_category function
        """
        # test get_relevant_category
        self.assertEqual(get_relevant_category(self.food_json), "en:cocoa-and-hazelnuts-spreads")

    def test_get_better_products(self):
        """
        Test the get_relevant_category function
        """
        # test get_relevant_category
        better_products = get_better_products(self.food_json)
        self.assertIn("en:cocoa-and-hazelnuts-spreads", better_products[0]['categories_hierarchy'])

    def test_get_relevant_category_unknown(self):
        self.mock_json = '{"product":{' \
            '"nutrition_grades":"e","code":"3017620429484"}}'
        self.food_json = json.loads(self.mock_json)
        self.assertEqual(get_relevant_category(self.food_json), "Unknown category")

    def test_get_better_products_unknown(self):
        self.mock_json = '{"product":{' \
            '"nutrition_grades":"e","code":"3017620429484"}}'
        self.food_json = json.loads(self.mock_json)
        self.assertEqual(get_better_products(self.food_json), [])
