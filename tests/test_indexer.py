import unittest
import os
import tempfile
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from src.indexer import InvertedIndex



#using temporary files to test the indexer functionality
class TestIndexer(unittest.TestCase):
    #create an empty indexer for each test
    def setUp(self):
        self.indexer = InvertedIndex()

    #test quote to ensure that it is tokenised
    def test_tokenise(self):
        #quote from the website to test
        text = "“The world as we have created, it's a PROCESS of our thinking.”"
        #should all be lowercase and s should be separate due to '
        expected = ['the', 'world', 'as', 'we', 'have', 'created', 'it',
                    's', 'a', 'process', 'of', 'our', 'thinking']
        
        #assert that the result is equal to what is expected
        result = self.indexer.tokenize(text)
        self.assertEqual(result, expected)

    #test word/frequency/position are recorded correctly in document
    def test_add_doc(self):
        #mock url and text to save before adding
        url = "https://quotes.toscrape.com/page/1/"
        text = "To be or not to be"
        self.indexer.add_document(url, text)

        #assert to/be/not
        self.assertIn('to', self.indexer.index)
        self.assertEqual(self.indexer.index['to'][url]['frequency'], 2)
        self.assertEqual(self.indexer.index['to'][url]['positions'], [0, 4])

        self.assertIn('be', self.indexer.index)
        self.assertEqual(self.indexer.index['be'][url]['frequency'], 2)
        self.assertEqual(self.indexer.index['be'][url]['positions'], [1, 5])

        self.assertIn('not', self.indexer.index)
        self.assertEqual(self.indexer.index['not'][url]['frequency'], 1)
        self.assertEqual(self.indexer.index['not'][url]['positions'], [3])

    #use a temp filepath to test index sent to JSON correctly
    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_filepath = os.path.join(temp_dir, "text_index.json")

            #add data then save and assert file created
            self.indexer.add_document("http://fake-save-url.com", "this is the test data to save")
            self.indexer.save(temp_filepath)
            self.assertTrue(os.path.exists(temp_filepath))

            #create new indexer and load from file
            new_indexer = InvertedIndex()
            self.assertEqual(new_indexer.index, {})
            new_indexer.load(temp_filepath)
            
            #check new loaded data matches original
            self.assertEqual(self.indexer.index, new_indexer.index)
            self.assertIn('save', new_indexer.index)
            self.assertEqual(new_indexer.index['save']['http://fake-save-url.com']['frequency'], 1)

if __name__ == '__main__':
    unittest.main()