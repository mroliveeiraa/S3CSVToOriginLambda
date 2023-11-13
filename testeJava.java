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


#############


import 1s0n
import logging
from src.utils.header import constroi header
import os
import requesta
‡ definindo tenant
TENANTS - ("radarj"
"tarifaspi")
der post caca ativacao contratos () :
‡ Chamar a api para cada tanant for tenant in TENANTS:
logging, info ("INICIANDO ATIVAÇAO DE CONIRATOS DO tenant :",
cenant)
header = constroi header (tenant)
response = requests. post (os, getenv ('URL CUCA CONTRATO'),
headers=header)
+ converter response de spring jeon para um objeto python
response cuca = json.loads (response.content or 11)!
； YEI1f1car gual foio rEtorno
1f response,status code ! = 202:
response jeon = (
istatus codel: response.status
_code,
"mensagem": "Algo deu errado ao ativar contracos do cenant:"-cenant
19901 ng.11501ze8pong-
cuca)
return zesponse 3son



###########



# Importando bibliotecas necessárias
import json
from unittest.mock import patch, MagicMock
import pytest
from post_ativacao_contratos import post_cuca_ativacao_contratos

# Teste para o caso de sucesso na ativação de contratos
def test_post_cuca_ativacao_contratos_success():
    # Usando o contexto do patch para substituir a função requests.post por um objeto simulado (mock)
    with patch("post_ativacao_contratos.requests.post") as mock_post:
        # Configurando o retorno do mock para simular uma resposta bem-sucedida (status_code=202)
        mock_post.return_value = MagicMock(status_code=202, content=json.dumps({}))
        # Chamando a função que está sendo testada
        result = post_cuca_ativacao_contratos()
        # Verificando se o status_code e a chave 'mensagem' estão presentes no resultado
        assert result["status_code"] == 202
        assert "mensagem" in result

# Teste para o caso de falha na ativação de contratos
def test_post_cuca_ativacao_contratos_failure():
    # Usando o contexto do patch para substituir a função requests.post por um objeto simulado (mock)
    with patch("post_ativacao_contratos.requests.post") as mock_post:
        # Configurando o retorno do mock para simular uma resposta de erro (status_code=500)
        mock_post.return_value = MagicMock(status_code=500, content=json.dumps({}))
        # Chamando a função que está sendo testada
        result = post_cuca_ativacao_contratos()
        # Verificando se o status_code e a chave 'mensagem' estão presentes no resultado
        assert result["status_code"] == 500
        assert "mensagem" in result

# Teste para o caso de exceção ao chamar a função
def test_post_cuca_ativacao_contratos_exception():
    # Usando o contexto do patch para substituir a função requests.post por um objeto simulado (mock)
    with patch("post_ativacao_contratos.requests.post") as mock_post:
        # Configurando o mock para lançar uma exceção simulada
        mock_post.side_effect = Exception("Mocked exception")
        # Verificando se a exceção é levantada ao chamar a função
        with pytest.raises(Exception):
            post_cuca_ativacao_contratos()




