import boto3

def delete_aerolinea(event, context):
    body = json.loads(event.get('body', '{}')) # Obtener el ID de la aerolínea
    id_aerolinea = event.get('id_aerolinea')

    # Conectar con DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_aerolineass')

    # Eliminar el ítem
    response = table.delete_item(
        Key={
            'id_aerolinea': id_aerolinea
        }
    )

    return {
        'statusCode': 200,
        'body': f'Aerolínea con id_aerolinea={id_aerolinea} eliminada correctamente.'
    }
