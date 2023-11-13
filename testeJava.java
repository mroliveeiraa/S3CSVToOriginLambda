import unittest
from unittest.mock import MagicMock
from lambda_function import lambda_handler  # Atualiza para o nome do arquivo correto

class TestPostAtivacaoContratos(unittest.TestCase):
    # Configuração inicial para os testes
    def setUp(self):
        # Cria um mock para o logger
        self.mock_logger = MagicMock()
        # Cria uma instância da função lambda_handler
        self.handler = lambda_handler
        # Atribui o mock_logger à instância do lambda_handler
        self.handler.logger = self.mock_logger

    # Teste para a função lambda_handler
    def test_lambda_handler(self):
        # Comentário indicando o teste específico
        # Cria um evento vazio
        event = {}
        # Chama a função lambda_handler com o evento e None como argumentos
        response = self.handler(event, None)

        # Verifica se o método info do logger foi chamado corretamente
        self.mock_logger.info.assert_called_once_with(response)

# Executa os testes
if __name__ == '__main__':
    unittest.main()
