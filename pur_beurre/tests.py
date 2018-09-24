from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase

from .models import Product
from django.urls import reverse
from .views import UserSavedProductsList


class ProductModelTests(TestCase):

    def test_str(self):
        """
        test str method for the model Product
        """
        product = Product(name="Test Name !", brand="Test Brand")
        self.assertIs(product.__str__(), "Test Name !")


class ViewsTests(TestCase):

    def test_homepage(self):
        """
        Test access to homepage
        """
        response = self.client.get(reverse('pur-beurre-index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Du gras")


class UserSavedProductsListTests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='Jean', email='jean@jean.com', password='passw0rd')

    def test_product_saved_logged_in(self):
        # Create an instance of a GET request.
        request = self.factory.get(reverse('saved-products'))

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Or you can simulate an anonymous user by setting request.user to
        # an AnonymousUser instance.
        # request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        response = UserSavedProductsList.as_view()(request)
        # Use this syntax for class-based views.
        # response = MyView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Produits sauvés par Jean")

    # doesn't work : RequestFactory can't follow redirects !
    # def test_product_saved_anon(self):
    #     request = self.factory.get(reverse('saved-products'))
    #     request.user = AnonymousUser()
    #     response = UserSavedProductsList.as_view()(request)
    #     # Use this syntax for class-based views.
    #     # response = MyView.as_view()(request)
    #     self.assertEqual(response.status_code, 200)
