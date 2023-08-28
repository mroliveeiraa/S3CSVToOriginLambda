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
