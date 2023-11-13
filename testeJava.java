from unittest.mock import patch
from src import post_ativacao_contratos

def test_lambda_handler():
    with patch('src.post_ativacao_contratos.post_cuca_ativacao_contratos') as mock_post:
        # Configurar o retorno simulado da função post_cuca_ativacao_contratos
        mock_post.return_value = "Mocked Response"

        # Chamar a função lambda_handler
        result = lambda_handler({}, {})

        # Verificar se a função post_cuca_ativacao_contratos foi chamada
        mock_post.assert_called_once()

        # Verificar se o resultado da função lambda_handler é o esperado
        assert result == "Mocked Response"
