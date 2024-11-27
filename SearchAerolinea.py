import boto3

def search_aerolinea(event, context):
    body = json.loads(event.get('body', '{}'))
    id_aerolinea = event.get('id_aerolinea')

    # Conectar con DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_aerolineas')

    # Buscar el ítem
    response = table.get_item(
        Key={
            'id_aerolinea': id_aerolinea
        }
    )

    # Verificar si el ítem fue encontrado
    if 'Item' in response:
        return {
            'statusCode': 200,
            'body': response['Item']
        }
    else:
        return {
            'statusCode': 404,
            'body': f'Aerolínea con id_aerolinea={id_aerolinea} no encontrada.'
        }
