from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase

from .models import Product
from django.urls import reverse
from .views import UserSavedProductsList
from users.views import profile


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

    def test_search(self):
        """
        Test access to search page without search terms
        """
        response = self.client.get(reverse('pur-beurre-results'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Entrez un produit à rechercher dans la barre de recherche")

    def test_search_arg(self):
        """
        Test access to search page with search terms
        """
        response = self.client.get(reverse('pur-beurre-results'), {'q': 'nutella'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Produits proposés pour la recherche: "nutella"')
        self.assertContains(response, 'Sélectionnez votre produit.')

    def test_substitutes(self):
        """
        Test page with substitutes after search page
        """
        response = self.client.get(reverse('pur-beurre-subsitutes'), {'code': '3017620429484'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nutella')

    def test_product_page(self):
        """
        Test page with substitutes after search page
        """
        response = self.client.get(reverse('pur-beurre-food'), {'code': '3017620429484'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nutella')
        self.assertContains(response, 'Ingrédients')


class UserLoggedIn(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='Jean', email='jean@jean.com', password='passw0rd')

    def test_user_profile_page_logged_in(self):
        request = self.factory.get(reverse('profile'))
        request.user = self.user
        response = profile(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email : jean@jean.com")

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


class AnonUser(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = AnonymousUser()

    def test_anon_user_profile_redirect(self):
        request = self.factory.get(reverse('profile'))
        request.user = self.user
        response = profile(request)
        # User should be redirected to log in page:
        self.assertEqual(response.status_code, 302)

    def test_anon_user_saved_products_redirect(self):
        request = self.factory.get(reverse('saved-products'))
        request.user = self.user
        response = profile(request)
        # User should be redirected to log in page:
        self.assertEqual(response.status_code, 302)

    def test_anon_user_save_redirect(self):
        request = self.factory.get(reverse('pur-beurre-save'))
        request.user = self.user
        response = profile(request)
        # User should be redirected to log in page:
        self.assertEqual(response.status_code, 302)
# tests :
# connexion de l'utilisateur
# recherche de produit
# recherche de produit non existant
# recherche de produit sans nutriscore
# recherche de produit sans catégorie
# recherche de substitut
# sauvegarde de produit
# suppression de sauvegarde
