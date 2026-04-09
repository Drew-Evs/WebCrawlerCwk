import unittest
import io
from unittest.mock import patch
from src.indexer import InvertedIndex
from src.search import Searcher

#use a prepopulated index to test the search
class TestSearcher(unittest.TestCase):
    def setUp(self):
        self.indexer = InvertedIndex()

        #injecting fake data
        self.indexer = InvertedIndex()
        self.indexer.index = {
            'good': {
                'http://fake-site.com/page1': {'frequency': 1, 'positions': [0]},
                'http://fake-site.com/page2': {'frequency': 1, 'positions': [5]}
            },
            'friends': {
                'http://fake-site.com/page2': {'frequency': 1, 'positions': [6]},
                'http://fake-site.com/page3': {'frequency': 1, 'positions': [1]}
            }
        }

        #initiate the searcher
        self.searcher = Searcher(self.indexer)

    #test a phrase of a single word on 2 pages
    def test_find_single_word(self):
        result = self.searcher.find_phrase("good")
        self.assertCountEqual(result, ['http://fake-site.com/page1', 'http://fake-site.com/page2'])
    
    #test a phrase that should only intersect on one page
    def test_find_multi_overlap(self):
        result = self.searcher.find_phrase("good firends")
        self.assertEqual(result, ['http://fake-site.com/page2'])

    #test returns empty list if one word missing
    def test_find_missing_word(self):
        result = self.searcher.find_phrase("good enemies")
        self.assertEqual(result, [])

    #get the output of the JSON string to terminal check formatted correctly
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_word_exists(self, mock_stdout):
        self.seracher.print_word("good")
        output = mock_stdout.getvalue()

        #check that terminal output has strings
        self.assertIn("Index Data Found for 'good'", output)
        self.assertIn("http://fake-site.com/page1", output)
    
    #check for a wrod not existing in the indexer
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_word_not_exists(self, mock_stdout):
        self.searcher.print_word("nonsense")
        output = mock_stdout.getvalue()
        self.assertIn("Word 'nonsense' not found in index", output)

if __name__ == '__main__':
    unittest.main()