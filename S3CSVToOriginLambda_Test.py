import unittest
from unittest.mock import Mock
from lambda_function import lambda_handler  # Importe a função Lambda do seu arquivo

class TestLambdaHandler(unittest.TestCase):
    def setUp(self):
        self.s3_client_mock = Mock()
        self.event = {
            'Records': [
                {
                    'cf': {
                        'request': {
                            'querystring': 'nome-do-arquivo.csv'
                        }
                    }
                }
            ]
        }

    def test_lambda_handler_success(self):
        self.s3_client_mock.get_object.return_value = {
            'Body': Mock(read=lambda: b'conteudo-do-arquivo-csv')
        }
        response = lambda_handler(self.event, None)
        self.assertEqual(response['status'], '200')

    def test_lambda_handler_file_not_found(self):
        self.s3_client_mock.get_object.side_effect = Exception('File not found')
        response = lambda_handler(self.event, None)
        self.assertEqual(response['status'], '404')

if __name__ == '__main__':
    unittest.main()
