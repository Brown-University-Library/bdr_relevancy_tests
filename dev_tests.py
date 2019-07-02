import os
import unittest
import requests
from tests import SOLR_URL, BDR_PUBLIC, escape_solr_special_chars, get_solr_results


TEST_DATA = [
        {'query': 'test:1', 'pid': 'test:1', 'lowest_ranking': 1},
        {'query': 'test:1125', 'pid': 'test:1125', 'lowest_ranking': 1},
        {'query': 'Cörper', 'pid': 'test:231377', 'lowest_ranking': 2},
        {'query': 'cörper', 'pid': 'test:231377', 'lowest_ranking': 2},
        {'query': 'Corper', 'pid': 'test:231377', 'lowest_ranking': 2},
        {'query': 'corper', 'pid': 'test:231377', 'lowest_ranking': 2},
        {'query': 'sampt beygefügter', 'pid': 'test:231377', 'lowest_ranking': 1},
        {'query': 'sampt beygefugter', 'pid': 'test:231377', 'lowest_ranking': 1},
        {'query': 'BETH0040', 'pid': 'test:233677', 'lowest_ranking': 1},
        {'query': 'beth0040', 'pid': 'test:233677', 'lowest_ranking': 1},
        {'query': 'openbsd', 'pid': 'test:233875', 'lowest_ranking': 1}, #verify title boost
        {'query': '111780829541025', 'pid': 'test:229775', 'lowest_ranking': 1}, #METS ID
        {'query': 'askb013692', 'pid': 'test:224428', 'lowest_ranking': 1}, #MODS ID
        {'query': 'Au-MP 1847 lf-1', 'pid': 'test:224428', 'lowest_ranking': 1}, #ASKB Call No.
    ]


class RelevancyTests(unittest.TestCase):

    def test_queries(self):
        for row in TEST_DATA:
            with self.subTest(row=row):
                query = row['query']
                results = get_solr_results(query, rows=row['lowest_ranking'])
                pids = [d['pid'] for d in results['response']['docs']]
                pid = row['pid']
                self.assertTrue(pid in pids, f'{pid} not in {pids} (query: "{query}")\n{results}')


if __name__ == '__main__':
    unittest.main()

