from django.test import TestCase
from django.urls import reverse
from .models import Category, Product

class ShopTests(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name='Books')
        self.prod = Product.objects.create(category=self.cat, title='Django for Beginners', price=500, inventory=5)

    def test_product_list(self):
        resp = self.client.get(reverse('shop:product_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Django for Beginners')

    def test_add_to_cart_and_checkout(self):
        add_url = reverse('shop:cart_add', args=[self.prod.id])
        self.client.post(add_url, {'quantity': 2})
        resp = self.client.get(reverse('shop:cart_detail'))
        self.assertContains(resp, 'Django for Beginners')
