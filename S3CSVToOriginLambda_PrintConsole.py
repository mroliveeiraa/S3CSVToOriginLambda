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
