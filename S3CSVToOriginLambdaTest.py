import logging
import re
import pytest
from unittest.mock import Mock, patch
from moto import mock_s3
import boto3

# Importar a função Lambda que você deseja testar (assumindo que está em um arquivo chamado lambda_function.py)
from lambda_function import lambda_handler

# Criar um logger de teste
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Definir uma função auxiliar para criar eventos de teste do CloudFront
def create_test_event(uri):
    return {
        'Records': [{
            'cf': {
                'request': {
                    'uri': uri
                }
            }
        }]
    }

@mock_s3
def test_lambda_handler_with_valid_csv():
    # Configurar o ambiente S3 simulado
    s3 = boto3.client('s3', region_name='us-east-1')
    s3.create_bucket(Bucket='xptoNomeS3')
    
    # Definir um objeto CSV simulado no bucket S3
    csv_content = 'Test CSV Content'
    s3.put_object(Bucket='xptoNomeS3', Key='site/test.csv', Body=csv_content)
    
    # Definir uma URL de teste
    test_uri = '/site/test.csv'
    
    # Criar um evento de teste
    event = create_test_event(test_uri)
    
    # Chamar a função Lambda
    response = lambda_handler(event, None)
    
    # Verificar se o arquivo foi encontrado
    assert response['status'] == '200'
    assert response['statusDescription'] == 'OK'
    assert response['headers']['content-type'][0]['value'] == 'text/csv'
    assert response['body'] == csv_content
    
    # Verificar se o logger registrou a mensagem correta
    assert logger.messages[0] == 'Arquivo site/test.csv encontrado no S3.'

# Teste para uma URL inválida
def test_lambda_handler_with_invalid_url():
    # Definir uma URL inválida
    test_uri = '/invalid-url'
    
    # Criar um evento de teste
    event = create_test_event(test_uri)
    
    # Chamar a função Lambda
    response = lambda_handler(event, None)
    
    # Verificar se o Lambda retorna um erro 404
    assert response['status'] == '404'
    assert response['statusDescription'] == 'Not Found'
    assert response['headers']['content-type'][0]['value'] == 'text/plain'
    assert response['body'] == 'Arquivo não encontrado'
    
    # Verificar se o logger registrou a mensagem de erro correta
    assert logger.messages[0] == 'URL inválida ou arquivo não encontrado.'

# Executar os testes com pytest
if __name__ == '__main__':
    pytest.main()
