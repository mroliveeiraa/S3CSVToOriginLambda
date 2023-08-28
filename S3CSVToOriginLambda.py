import json
import boto3

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Obter o nome do arquivo do parâmetro passado no URL do CloudFront
    file_name = event['Records'][0]['cf']['request']['querystring']

    # Definir o nome do bucket S3
    bucket_name = 'seu-bucket-s3-aqui'

    try:
        # Fazer o download do arquivo .csv do bucket S3
        response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        file_content = response['Body'].read()

        # Criar uma resposta para o CloudFront
        response = {
            'status': '200',
            'statusDescription': 'OK',
            'headers': {
                'content-type': [{
                    'key': 'Content-Type',
                    'value': 'text/csv'
                }],
                'cache-control': [{
                    'key': 'Cache-Control',
                    'value': 'max-age=3600'
                }],
            },
            'body': file_content,
            'bodyEncoding': 'base64'
        }
    except Exception as e:
        response = {
            'status': '404',
            'statusDescription': 'Not Found'
        }

    return response
