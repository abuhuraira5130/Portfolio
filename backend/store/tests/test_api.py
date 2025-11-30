from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from store.models import Product, Collection, Customer

class ProductTests(APITestCase):
    def setUp(self):
        self.collection = Collection.objects.create(title='Test')
        Product.objects.create(title='P1', slug='p1', price=10, inventory=5, collection=self.collection)
        Product.objects.create(title='P2', slug='p2', price=20, inventory=3, collection=self.collection)

    def test_list_products(self):
        url = reverse('product-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('results' in resp.data)
        self.assertEqual(len(resp.data['results']), 2)

class AdminProductCreateTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
        self.token = Token.objects.create(user=self.admin)
        self.collection = Collection.objects.create(title='AdminTest')

    def test_admin_create_product(self):
        url = reverse('product-list')
        payload = {
            'title': 'NewProd',
            'slug': 'newprod',
            'price': '99.99',
            'inventory': 10,
            'collection': self.collection.id,
            'featured': False,
            'description': ''
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Product.objects.count(), 1)

class OrderCreateTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@example.com', 'userpass')
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(user=self.user, first_name='U', last_name='S', email='user@example.com')
        c = Collection.objects.create(title='C')
        self.p1 = Product.objects.create(title='P1', slug='p1', price=5, inventory=10, collection=c)
        self.p2 = Product.objects.create(title='P2', slug='p2', price=7, inventory=10, collection=c)

    def test_create_order(self):
        url = reverse('order-list')
        payload = {
            'items': [
                {'product': self.p1.id, 'quantity': 2, 'unit_price': str(self.p1.price)},
                {'product': self.p2.id, 'quantity': 1, 'unit_price': str(self.p2.price)}
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertIn('total', resp.data)