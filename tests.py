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

    def test_queries(self):
        for row in TEST_DATA:
            with self.subTest(row=row):
                query = escape_solr_special_chars(row['query'])
                solr_query = f'discover:{BDR_PUBLIC} AND {query}'
                r = requests.get(f'{SOLR_URL}select/?q={solr_query}&fl=pid&wt=json&rows={row["lowest_ranking"]}')
                if not r.ok:
                    raise Exception(f'{r.status_code} - {r.content.decode("utf8")} - {query}')
                results = r.json()
                pids = [d['pid'] for d in results['response']['docs']]
                pid = row['pid']
                self.assertTrue(pid in pids, f'{pid} not in {pids} (query: "{query}")')


if __name__ == '__main__':
    unittest.main()

