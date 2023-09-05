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



///
import logging
import re
from unittest.mock import Mock, patch
import pytest

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

# Mock da função get_object do cliente S3
@patch('boto3.client')
def test_lambda_handler_with_valid_csv(mock_boto3_client):
    # Configurar o mock para o cliente S3
    mock_s3_client = Mock()
    mock_boto3_client.return_value = mock_s3_client
    
    # Configurar o retorno simulado para get_object
    mock_s3_client.get_object.return_value = {
        'Body': Mock(read=Mock(return_value='CSV Content'))
    }
    
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
    assert response['body'] == 'CSV Content'
    
    # Verificar se o logger registrou a mensagem correta
    assert logger.messages[0] == f'Arquivo site/test.csv encontrado no S3.'

# Teste para uma URL inválida
@patch('boto3.client')
def test_lambda_handler_with_invalid_url(mock_boto3_client):
    # Configurar o mock para o cliente S3
    mock_s3_client = Mock()
    mock_boto3_client.return_value = mock_s3_client
    
    # Simular uma exceção ao buscar o objeto S3 (para simular um erro)
    mock_s3_client.get_object.side_effect = Exception('Object not found')
    
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




/////////////:
import pytest
from your_module import Xpto  # Importe sua classe Xpto

def test_s3_method(mocker):
    # Crie um mock para o cliente S3
    mock_s3_client = mocker.patch('boto3.client')

    # Configure o comportamento do mock para a chamada get_object
    mock_get_object = mock_s3_client.return_value.get_object
    mock_get_object.return_value = {'Key': 'Value'}

    # Crie uma instância da classe Xpto
    xpto = Xpto()

    # Chame o método s3_method
    response = xpto.s3_method('my_bucket', 'my_key')

    # Verifique se o método foi chamado corretamente
    mock_get_object.assert_called_once_with(Bucket='my_bucket', Key='my_key')

    # Verifique o resultado do método
    assert response == {'Key': 'Value'}




///////
import pytest
import boto3
from unittest.mock import Mock
from lambda_function import lambda_handler

# Use o fixture pytest-mock para configurar o objeto mock do boto3.client('s3')
@pytest.fixture
def s3_client_mock(mocker):
    return mocker.patch('boto3.client')

def test_valid_csv_request(mocker, s3_client_mock):
    # Configurar o comportamento esperado para o cliente S3 mockado
    s3_client_mock.return_value.get_object.return_value = {
        'Body': {
            'read.return_value': 'Conteúdo CSV mockado'
        }
    }

    event = {
        'Records': [
            {
                'cf': {
                    'request': {
                        'uri': '/site/nomedoArquivo.csv'
                    }
                }
            }
        ]
    }

    # Chamar a função Lambda com o evento de teste
    response = lambda_handler(event, None)

    # Verificar se o cliente S3 foi chamado corretamente
    s3_client_mock.assert_called_once_with('s3')

    # Verificar se o método get_object do cliente S3 foi chamado corretamente
    s3_client_mock.return_value.get_object.assert_called_once_with(
        Bucket='xptoNomeS3',
        Key='site/nomedoArquivo.csv'
    )

    # Verificar se a resposta está correta
    assert response['status'] == '200'
    assert response['headers']['content-type'][0]['value'] == 'text/csv'
    assert response['body'] == 'Conteúdo CSV mockado'


/////////


import boto3
from unittest.mock import Mock
from lambda_function import lambda_handler

def test_valid_csv_request():
    event = {
        'Records': [
            {
                'cf': {
                    'request': {
                        'uri': '/site/nomedoArquivo.csv'
                    }
                }
            }
        ]
    }

    # Criar um cliente S3 mockado
    s3_client_mock = Mock()

    # Configurar o comportamento esperado para o cliente S3
    s3_client_mock.get_object.return_value = {
        'Body': {
            'read.return_value': 'Conteúdo CSV mockado'
        }
    }

    # Substituir o cliente S3 real pelo mock
    boto3.client = Mock(return_value=s3_client_mock)

    # Configurar o logger para capturar mensagens de log
    logger_mock = Mock()
    lambda_handler.logger = logger_mock

    # Chamar a função Lambda com o evento de teste
    response = lambda_handler(event, None)

    # Verificar se o cliente S3 foi chamado corretamente
    s3_client_mock.get_object.assert_called_once_with(
        Bucket='xptoNomeS3',
        Key='site/nomedoArquivo.csv'
    )

    # Verificar se o logger registrou a mensagem correta
    logger_mock.info.assert_called_with('Arquivo site/nomedoArquivo.csv encontrado no S3.')

    # Verificar se a resposta está correta
    assert response['status'] == '200'
    assert response['headers']['content-type'][0]['value'] == 'text/csv'
    assert response['body'] == 'Conteúdo CSV mockado'

def test_invalid_csv_request():
    event = {
        'Records': [
            {
                'cf': {
                    'request': {
                        'uri': '/site/arquivo_invalido.txt'
                    }
                }
            }
        ]
    }

    # Criar um cliente S3 mockado
    s3_client_mock = Mock()

    # Substituir o cliente S3 real pelo mock
    boto3.client = Mock(return_value=s3_client_mock)

    # Configurar o logger para capturar mensagens de log
    logger_mock = Mock()
    lambda_handler.logger = logger_mock

    # Chamar a função Lambda com o evento de teste
    response = lambda_handler(event, None)

    # Verificar se o cliente S3 não foi chamado
    s3_client_mock.get_object.assert_not_called()

    # Verificar se o logger registrou a mensagem de erro correta
    logger_mock.error.assert_called_with('URL inválida ou arquivo não encontrado.')

    # Verificar se a resposta está correta
    assert response['status'] == '404'
    assert response['body'] == 'Arquivo não encontrado'


///////////

import boto3
from unittest.mock import Mock
from lambda_function import lambda_handler

def test_valid_csv_request():
    event = {
        'Records': [
            {
                'cf': {
                    'request': {
                        'uri': '/site/nomedoArquivo.csv'
                    }
                }
            }
        ]
    }

    # Configurar o comportamento esperado para o cliente S3
    s3_client_mock = Mock()
    s3_client_mock.get_object.return_value = {
        'Body': {
            'read.return_value': 'Conteúdo CSV mockado'
        }
    }
    lambda_handler.s3_client = s3_client_mock

    # Configurar o logger para capturar mensagens de log
    logger_mock = Mock()
    lambda_handler.logger = logger_mock

    # Chamar a função Lambda com o evento de teste
    response = lambda_handler(event, None)

    # Verificar se o cliente S3 foi chamado corretamente
    s3_client_mock.get_object.assert_called_once_with(
        Bucket='xptoNomeS3',
        Key='site/nomedoArquivo.csv'
    )

    # Verificar se o logger registrou a mensagem correta
    logger_mock.info.assert_called_with('Arquivo site/nomedoArquivo.csv encontrado no S3.')

    # Verificar se a resposta está correta
    assert response['status'] == '200'
    assert response['headers']['content-type'][0]['value'] == 'text/csv'
    assert response['body'] == 'Conteúdo CSV mockado'

def test_invalid_csv_request():
    event = {
        'Records': [
            {
                'cf': {
                    'request': {
                        'uri': '/site/arquivo_invalido.txt'
                    }
                }
            }
        ]
    }

    # Configurar o logger para capturar mensagens de log
    logger_mock = Mock()
    lambda_handler.logger = logger_mock

    # Chamar a função Lambda com o evento de teste
    response = lambda_handler(event, None)

    # Verificar se o logger registrou a mensagem de erro correta
    logger_mock.error.assert_called_with('URL inválida ou arquivo não encontrado.')

    # Verificar se a resposta está correta
    assert response['status'] == '404'
    assert response['body'] == 'Arquivo não encontrado'





//////////////
{
    "Records": [
        {
            "cf": {
                "config": {
                    "distributionDomainName": "xptoLink.com.br"
                },
                "request": {
                    "uri": "/nomedoArquivo.csv"
                }
            }
        }
    ]
}


////////////




import boto3
import logging

s3_client = boto3.client('s3')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Obter o nome do arquivo do parâmetro passado no URL do CloudFront
    file_name = event['Records'][0]['cf']['request']['querystring']

    # Definir o nome do bucket S3
    bucket_name = 'seu-bucket-s3-aqui'

    try:
        # Fazer o download do arquivo .csv do bucket S3
        response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        file_content = response['Body'].read().decode('utf-8')

        # Imprimir o conteúdo completo do arquivo no log da aplicação
        logger.info("Conteúdo do arquivo %s:\n%s", file_name, file_content)
        
        # Criar uma resposta para o CloudFront
        response = {
            'status': '200',
            'statusDescription': 'OK',
            'headers': {
                'content-type': [{
                    'key': 'Content-Type',
                    'value': 'text/plain'
                }],
                'cache-control': [{
                    'key': 'Cache-Control',
                    'value': 'max-age=3600'
                }],
            },
            'body': 'Arquivo processado com sucesso!'
        }
    except Exception as e:
        logger.error("Erro ao processar o arquivo %s: %s", file_name, str(e))
        response = {
            'status': '500',
            'statusDescription': 'Internal Server Error'
        }

    return response

____________________________

import boto3
import logging

s3_client = boto3.client('s3')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Nome do arquivo e pasta no bucket S3
    folder_name = 'site'
    file_name = 'radarpj-2023-8-23.csv'
    bucket_name = 'seu-bucket-s3-aqui'

    try:
        # Fazer o download do arquivo .csv do bucket S3
        response = s3_client.get_object(Bucket=bucket_name, Key=f'{folder_name}/{file_name}')
        file_content = response['Body'].read().decode('utf-8')

        # Imprimir o conteúdo completo do arquivo no log da aplicação
        logger.info("Conteúdo do arquivo %s/%s:\n%s", folder_name, file_name, file_content)
        
        # Criar uma resposta para o CloudFront
        response = {
            'status': '200',
            'statusDescription': 'OK',
            'headers': {
                'content-type': [{
                    'key': 'Content-Type',
                    'value': 'text/plain'
                }],
                'cache-control': [{
                    'key': 'Cache-Control',
                    'value': 'max-age=3600'
                }],
            },
            'body': 'Arquivo processado com sucesso!'
        }
    except Exception as e:
        logger.error("Erro ao processar o arquivo %s/%s: %s", folder_name, file_name, str(e))
        response = {
            'status': '500',
            'statusDescription': 'Internal Server Error'
        }

    return response


---------------------------------

import boto3
import logging

s3_client = boto3.client('s3')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # Nome do arquivo e pasta no bucket S3
        folder_name = 'site'
        file_name = 'XPTO.csv'
        bucket_name = 'nomeBucket'
        
        # Imprimir informações sobre o início do processamento
        logger.info("Iniciando acesso ao arquivo %s/%s no bucket %s", folder_name, file_name, bucket_name)
        
        # Fazer o download do arquivo .csv do bucket S3
        logger.info("Baixando o arquivo %s/%s...", folder_name, file_name)
        response = s3_client.get_object(Bucket=bucket_name, Key=f'{folder_name}/{file_name}')
        file_content = response['Body'].read().decode('utf-8')
        
        # Imprimir informações sobre o sucesso do download
        logger.info("Download do arquivo %s/%s concluído com sucesso", folder_name, file_name)
        
        # Imprimir o conteúdo do arquivo
        logger.info("Conteúdo do arquivo:\n%s", file_content)
        
        # Restante do código...
    except Exception as e:
        logger.error("Erro ao processar o arquivo %s/%s: %s", folder_name, file_name, str(e))
        response = {
            'status': '500',
            'statusDescription': 'Internal Server Error'
        }

    return response











-------------------111-1-----------

import json
import logging
import os
import urllib.parse
import boto3
from botocore.exceptions import NoCredentialsError

# Configurar o registro de logs
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Extrair informações da solicitação do CloudFront
    request = event['Records'][0]['cf']['request']
    s3_bucket = 'xptoNomeBucket'
    s3_key = 'xptoSite/' + request['uri']  # Caminho completo do arquivo .csv
    
    try:
        # Inicializar o cliente S3
        s3_client = boto3.client('s3')

        # Verificar se o arquivo .csv existe no S3
        s3_client.head_object(Bucket=s3_bucket, Key=s3_key)

        # Configurar a resposta para o CloudFront
        response = {
            'status': '200',
            'statusDescription': 'OK',
            'headers': {
                'content-type': [{'key': 'Content-Type', 'value': 'text/csv'}],
                'content-disposition': [{'key': 'Content-Disposition', 'value': 'attachment; filename="xptoArquivo.csv"'}]
            },
            'body': ''
        }

        return response
    except NoCredentialsError:
        logger.error("As credenciais não estão configuradas corretamente.")
        return {
            'status': '500',
            'statusDescription': 'Internal Server Error'
        }
    except Exception as e:
        logger.error(f"Erro ao processar a solicitação: {str(e)}")
        return {
            'status': '404',
            'statusDescription': 'Not Found'
        }

///////////////////////////////


import boto3
import logging
import re

# Configurar o cliente S3
s3_client = boto3.client('s3')

# Configurar o logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Obter a solicitação do CloudFront
    request = event['Records'][0]['cf']['request']
    uri = request['uri']
    
    # Extrair o nome do arquivo da URL
    match = re.search(r'/([^/]+\.csv)$', uri)
    
    if match:
        # Nome do arquivo .csv encontrado na URL
        filename = match.group(1)
        
        # Nome do bucket S3 e caminho para o arquivo .csv
        s3_bucket = 'xptoNomeS3'
        s3_key = 'site/' + filename
        
        try:
            # Obter o arquivo .csv do S3
            response = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)
            
            # Ler o conteúdo do arquivo .csv
            csv_content = response['Body'].read().decode('utf-8')
            
            # Registrar que o arquivo foi encontrado
            logger.info(f'Arquivo {s3_key} encontrado no S3.')
            
            # Configurar a resposta para o CloudFront
            return {
                'status': '200',
                'statusDescription': 'OK',
                'headers': {
                    'content-type': [{'key': 'Content-Type', 'value': 'text/csv'}],
                    'content-disposition': [{'key': 'Content-Disposition', 'value': f'attachment; filename="{filename}"'}]
                },
                'body': csv_content
            }
        except Exception as e:
            # Registrar erros
            logger.error(f'Erro ao buscar o arquivo {s3_key} no S3: {str(e)}')
    
    # Se a URL não corresponder ou ocorrer um erro, retornar um erro 404
    logger.error('URL inválida ou arquivo não encontrado.')
    return {
        'status': '404',
        'statusDescription': 'Not Found',
        'headers': {
            'content-type': [{'key': 'Content-Type', 'value': 'text/plain'}],
        },
        'body': 'Arquivo não encontrado'
    }






testes unitsrios



import pytest
from unittest.mock import Mock
from your_lambda_module import lambda_handler  # Substitua 'your_lambda_module' pelo nome do seu módulo Lambda

@pytest.fixture
def s3_client_mock():
    return Mock()

@pytest.fixture
def logger_mock():
    return Mock()

def test_valid_csv_request(s3_client_mock, logger_mock):
    event = {
        'Records': [
            {
                'cf': {
                    'request': {
                        'uri': '/site/nomedoArquivo.csv'
                    }
                }
            }
        ]
    }

    # Configurar o comportamento esperado para o cliente S3
    s3_client_mock.get_object.return_value = {
        'Body': {
            'read.return_value': 'Conteúdo CSV mockado'
        }
    }

    # Substituir o cliente S3 real pelo mock
    lambda_handler.s3_client = s3_client_mock

    # Configurar o logger para capturar mensagens de log
    lambda_handler.logger = logger_mock

    # Chamar a função Lambda com o evento de teste
    response = lambda_handler.lambda_handler(event, None)

    # Verificar se o cliente S3 foi chamado corretamente
    s3_client_mock.get_object.assert_called_once_with(
        Bucket='xptoNomeS3',
        Key='site/nomedoArquivo.csv'
    )

    # Verificar se o logger registrou a mensagem correta
    logger_mock.info.assert_called_with('Arquivo site/nomedoArquivo.csv encontrado no S3.')

    # Verificar se a resposta está correta
    assert response['status'] == '200'
    assert response['headers']['content-type'][0]['value'] == 'text/csv'
    assert response['body'] == 'Conteúdo CSV mockado'

def test_invalid_csv_request(logger_mock):
    event = {
        'Records': [
            {
                'cf': {
                    'request': {
                        'uri': '/site/arquivo_invalido.txt'
                    }
                }
            }
        ]
    }

    # Configurar o logger para capturar mensagens de log
    lambda_handler.logger = logger_mock

    # Chamar a função Lambda com o evento de teste
    response = lambda_handler.lambda_handler(event, None)

    # Verificar se o logger registrou a mensagem de erro correta
    logger_mock.error.assert_called_with('URL inválida ou arquivo não encontrado.')

    # Verificar se a resposta está correta
    assert response['status'] == '404'
    assert response['body'] == 'Arquivo não encontrado'
