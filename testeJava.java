import unittest
from unittest.mock import MagicMock
from se import post_ativacao_contratos

class TestPostAtivacaoContratos(unittest.TestCase):

    def setUp(self):
        self.mock_logger = MagicMock()
        self.handler = lambda_handler()
        self.handler.logger = self.mock_logger

    def test_lambda_handler(self):
        event = {}
        response = self.handler(event, None)
        
        self.mock_logger.info.assert_called_once_with(response)

if __name__ == '__main__':
    unittest.main()
