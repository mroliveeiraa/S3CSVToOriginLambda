from unittest.mock import patch
from lambda_function import lambda_handler

def test_lambda_handler():
    # Configurar o ambiente de teste com um mock para post_cuca_ativacao_contratos
    with patch('lambda_function.post_ativacao_contratos.post_cuca_ativacao_contratos') as mock_post:
        # Configurar o retorno simulado da função post_cuca_ativacao_contratos
        mock_post.return_value = "Mocked Response"

        # Chamar a função lambda_handler com argumentos fictícios
        result = lambda_handler({}, {})

        # Verificar se a função post_cuca_ativacao_contratos foi chamada exatamente uma vez
        mock_post.assert_called_once()

        # Verificar se o resultado da função lambda_handler é o esperado ("Mocked Response")
        assert result == "Mocked Response"
