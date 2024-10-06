from django.test import TestCase

from django.db import connection
from django.test.utils import CaptureQueriesContext


class TestCalls(TestCase):
    fixtures = ["menu/tests/menu_fixtures.json"]

    def test_menu_all_makes_minimal_queries(self):
        # Assemble: declare max number of db queries
        max_queries = 3

        with CaptureQueriesContext(connection) as context:
            # Act: Access url
            response = self.client.get("/menu/all/")
            # Assert: View is successful (aeb 200 status code) and queries made,
            # but query count is minimal
            self.assertEqual(response.status_code, 200)
            self.assertGreater(len(context.captured_queries), 0)
            self.assertLessEqual(len(context.captured_queries), max_queries)

    # # Alternative Style is not counting the queries, unless set DEBUG to True
    # def test_menu_all_makes_minimal_queries(self):
    #     with self.settings(DEBUG=True):
    #         # Assemble: declare max number of db queries
    #         # and get baseline query count
    #         max_queries = 3
    #         num_queries_start = len(connection.queries)

    #         # Act: Access url, get new query count and subtract baseline
    #         response = self.client.get("/menu/all/")
    #         num_queries_new = len(connection.queries)
    #         query_count = num_queries_new - num_queries_start

    #         # Assert: View is successful (aeb 200 status code) and queries made,
    #         # but query count is minimal
    #         self.assertEqual(response.status_code, 200)
    #         self.assertGreater(len(query_count), 0)
    #         self.assertLessEqual(len(query_count), max_queries)
