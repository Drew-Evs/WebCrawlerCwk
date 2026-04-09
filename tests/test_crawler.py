import unittest
from unittest.mock import patch, MagicMock
from src.crawler import build_crawler

#using mocking to simulate website repsonse

class TestCrawler(unittest.TestCase):
    #simulate the web requests and sleep
    @patch('src.crawler.requests.get')
    @patch('src.crawler.time.sleep')
    def test_crawler_success(self, mock_sleep, mock_get):
        #mock response setup 1st create fake html form site
        mock_html = """
            <html>
                <body>
                    <span class="text">"The world as we have created it is a process of our thinking."</span>
                    <small class="author">Albert Einstein</small>
                </body>
            </html>
            """
        
        #configure mocked get requests
        mock_response = MagicMock()
        mock_response.text = mock_html
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        #run test function with a fake url
        test_url = "http://fake-test-website.com"
        result = build_crawler(test_url)

        #assert requests.get was called and sleep aswell
        mock_get.assert_called_with(test_url)
        mock_sleep.assert_called_with(6)

if __name__ == '__main__':
    unittest.main()
