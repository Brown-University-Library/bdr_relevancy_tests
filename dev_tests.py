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

    def _get_solr_results(self, query, rows=10):
        query = escape_solr_special_chars(query)
        perms_query = f'discover:{BDR_PUBLIC}'
        r = requests.get(f'{SOLR_URL}select/?q={query}&fq={perms_query}&fl=pid&wt=json&rows={rows}')
        if not r.ok:
            raise Exception(f'{r.status_code} - {r.content.decode("utf8")} - {query}')
        results = r.json()
        return results

    def test_queries(self):
        for row in TEST_DATA:
            with self.subTest(row=row):
                query = row['query']
                results = self._get_solr_results(query, rows=row['lowest_ranking'])
                pids = [d['pid'] for d in results['response']['docs']]
                pid = row['pid']
                self.assertTrue(pid in pids, f'{pid} not in {pids} (query: "{query}")')

    def test_more_words_narrow_the_results(self):
        '''If q.op is 'OR', then more terms widen the results - it's a union of results for all the terms.
        If q.op is 'AND', then more terms narrow the results - it's an intersection of results.'''
        query1 = 'africa'
        query2 = 'africa french soldiers'
        results1 = self._get_solr_results(query1)
        results2 = self._get_solr_results(query2)
        self.assertGreater(results1['response']['numFound'], results2['response']['numFound'])


if __name__ == '__main__':
    unittest.main()

