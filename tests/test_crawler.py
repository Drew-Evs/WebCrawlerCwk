import unittest
from unittest.mock import patch, MagicMock, call
from src.crawler import build_crawler

#using mocking to simulate website repsonse

class TestCrawler(unittest.TestCase):
    #simulate the web requests and sleep
    @patch('src.crawler.requests.get')
    @patch('src.crawler.time.sleep')
    def test_crawler_success(self, mock_sleep, mock_get):
        #mock response setup 1st create fake html form site
        #1 with button next with no button
        mock_html_1 = """
        <html>
            <body>
                <span class="text">"The world as we have created it is a process of our thinking."</span>
                <small class="author">Albert Einstein</small>
            </body>

            <li class="next">
                <a href="/page/2/">Next <span aria-hidden="true">&rarr;</span></a>
            </li>
        </html>
        """
        
        mock_html_2 = """
        <html>
            <body>
                <span class="text">"It is our choices, Harry, that show what we truly are."</span>
                <small class="author">J.K. Rowling</small>
            </body>
        </html>
        """
        
        #configure mocked get requests
        mock_response_1 = MagicMock()
        mock_response_1.text = mock_html_1
        mock_response_1.status_code = 200

        mock_response_2 = MagicMock()
        mock_response_2.text = mock_html_2
        mock_response_2.status_code = 200

        #using side effect to return page 1 then page 2
        mock_get.side_effect = [mock_response_1, mock_response_2]

        #run test function with a fake url
        test_url = "http://fake-test-website.com"
        result = build_crawler(test_url)

        #assert requests.get was called and sleep with multiple pages
        expected_calls = [
            call("http://fake-test-website.com"),
            call("http://fake-test-website.com/page/2/")
        ]

        #check called twice for each page
        mock_get.assert_has_calls(expected_calls, any_order=False)
        self.assertEqual(mock_get.call_count, 2)
        self.assertEqual(mock_sleep.call_count, 2)

if __name__ == '__main__':
    unittest.main()
