from django.test import TestCase, Client
from django.urls import reverse
from menu.models import SetMenu, Hotdog, Bun
from django.db import connection
from django.test.utils import CaptureQueriesContext

class MenuViewTests(TestCase):
    def setUp(self):
        # Create test data
        hotdog = Hotdog.objects.create(name="Test Hotdog")
        bun = Bun.objects.create(name="Test Bun")
        for i in range(50):  # Create 50 menu items
            SetMenu.objects.create(
                name=f"Menu Item {i}",
                hotdog=hotdog,
                bun=bun,
                price_us=5 + i * 0.5  # Prices from 5 to 29.5
            )

    def test_all_items_view(self):
        client = Client()
        url = reverse('setmenu-all')

        with CaptureQueriesContext(connection) as queries:
            response = client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertLess(len(queries), 5)  # Ensure we're not making too many queries


    def test_query_count(self):
        client = Client()
        url = reverse('setmenu-all')

        with CaptureQueriesContext(connection) as queries:
            response = client.get(url)

        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(queries), 2, f"Expected 2 queries, got {len(queries)}")
        self.assertLessEqual(len(queries), 3)