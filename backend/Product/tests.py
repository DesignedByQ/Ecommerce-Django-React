from django.test import TestCase
from .models import Product, Tag
from http import HTTPStatus
 
class ProductModelTest(TestCase):

    #each method counts at one test

    def test_date_type_of_objects(self):

        mock_product = Product.objects.create(
            sku = 123,
            name = "Test Product",
            description = "Test Desc",
            has_sizes = True,
            inventory_count = 100,
            retail_price = 9.99,
            image_url = "Test URL",
            rating = 5.0
        )

        self.assertEqual(str(mock_product), mock_product.name)

    def test_product_model_exists(self):

        Product.objects.create(
            sku = 123,
            name = "Test Product",
            description = "Test Desc",
            has_sizes = True,
            inventory_count = 100,
            retail_price = 9.99,
            image_url = "Test URL",
            rating = 5.0
        )

        products = Product.objects.count()
        #or products = Product.objects.all()

        self.assertEqual(products, 1)
        #or self.assertEqual(len(products), 1)

    def test_add_tags_to_product_creates_tag_in_db(self):
        
        product = Product.objects.create(
            sku = 123,
            name = "Test Product",
            description = "Test Desc",
            has_sizes = True,
            inventory_count = 100,
            retail_price = 9.99,
            image_url = "Test URL",
            rating = 5.0
        )

        tag1 = Tag.objects.create(
            name='Tag 1',
            friendly_name='Friendly Tag 1'
        )

        tag2 = Tag.objects.create(
            name='Tag 2',
            friendly_name='Friendly Tag 2'
        )

        product.tags.set([tag1, tag2])

        self.assertEqual(str(tag1), tag1.name)
        self.assertEqual(str(tag2), tag2.name)

        product1 = product.tags.all()
        print(len(product1))
        self.assertEqual(len(product1), 2)

#template view tests
class HomepageTest(TestCase):
    
    def setUp(self) -> None:

        product1 = Product.objects.create(
            sku = 123,
            name = "Test Product1",
            description = "Test Desc",
            has_sizes = True,
            inventory_count = 100,
            retail_price = 9.99,
            image_url = "Test URL",
            rating = 5.0
        )

        product2 = Product.objects.create(
            sku = 12345,
            name = "Test Product2",
            description = "Test Desc",
            has_sizes = True,
            inventory_count = 100,
            retail_price = 9.99,
            image_url = "Test URL",
            rating = 5.0
        )

    def test_homepage_returns_correct_response(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'products/index.html')
        self.assertEqual(response.status_code, HTTPStatus.OK)    

    def test_homepage_returns_product_list(self):
        response = self.client.get("/")

        self.assertContains(response, 'Test Product1')
        self.assertContains(response, 'Test Product2')
        

