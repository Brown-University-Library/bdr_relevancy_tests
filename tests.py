import os
import unittest
import requests


TEST_DATA = [
        {'query': 'bdr:1', 'pid': 'bdr:1', 'lowest_ranking': 1},
        {'query': 'africa', 'pid': 'bdr:41266', 'lowest_ranking': 5},
        {'query': 'linux', 'pid': 'bdr:386312', 'lowest_ranking': 5},
        {'query': 'abraham lincoln', 'pid': 'bdr:75649', 'lowest_ranking': 5},
    ]

SOLR_URL = os.environ['SOLR_URL']
BDR_PUBLIC = 'BDR_PUBLIC'
SOLR_SPECIAL_CHARS = [':']


def escape_solr_special_chars(s):
    for c in SOLR_SPECIAL_CHARS:
        s = s.replace(c, fr'\{c}')
    return s


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

