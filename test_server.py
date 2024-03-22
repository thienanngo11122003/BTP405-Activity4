import http
import unittest
from http.server import HTTPServer
from server import SimpleHTTPRequestHandler
import http.client
import json
import threading

class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_address = ('localhost', 8000)
        cls.server = HTTPServer(cls.server_address, SimpleHTTPRequestHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

    def test_get_method(self):
        # Connect to the server and send a GET request
        connection = http.client.HTTPConnection(*self.server_address)
        connection.request('GET', '/')
        response = connection.getresponse()

        # Read and Decode the response
        data = response.read().decode()
        connection.close()

        # Check that the response is as expected
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'application/json')

        # Parse the JSON data and verify the content
        response_data = json.loads(data)
        self.assertEqual(response_data, {'message': 'This is a GET request response'})

    def test_post_method(self):
        # Define the payload to be sent in the POST request
        payload = json.dumps({'key': 'value'})

        # Connect to the server and send a POST request with the payload
        connection = http.client.HTTPConnection(*self.server_address)
        headers = {'Content-Type': 'application/json'}
        connection.request('POST', '/', body=payload, headers=headers)
        response = connection.getresponse()

        # Read and Decode the response
        data = response.read().decode()
        connection.close()

        # Check that the response is as expected
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'application/json')

        # The server echoes back the received data in this case
        expected_response = {'received': {'key': 'value'}}

        # Parse the JSON data and verify the content
        response_data = json.loads(data)
        self.assertEqual(response_data, expected_response)


if __name__ == '__main__':
    unittest.main()
