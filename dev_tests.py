import os
import unittest
import requests
from tests import SOLR_URL, BDR_PUBLIC, escape_solr_special_chars, get_solr_results


TEST_DATA = [
        {'query': 'test:1125', 'pid': 'test:1125', 'lowest_ranking': 1},
        {'query': 'Cörper', 'pid': 'test:231377', 'lowest_ranking': 2},
        {'query': 'Corper', 'pid': 'test:231377', 'lowest_ranking': 2},
    ]


class RelevancyTests(unittest.TestCase):

    def test_queries(self):
        for row in TEST_DATA:
            with self.subTest(row=row):
                query = row['query']
                results = get_solr_results(query, rows=row['lowest_ranking'])
                pids = [d['pid'] for d in results['response']['docs']]
                pid = row['pid']
                self.assertTrue(pid in pids, f'{pid} not in {pids} (query: "{query}")')


if __name__ == '__main__':
    unittest.main()

