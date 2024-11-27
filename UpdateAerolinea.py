import boto3

def update_aerolinea(event, context):
    body = json.loads(event.get('body', '{}'))
    id_aerolinea = event.get('id_aerolinea')
    atributos_actualizar = event.get('atributos')  # Diccionario con los atributos y valores a actualizar

    # Conectar con DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_aerolineass')

    # Construir la expresión de actualización
    update_expression = "SET " + ", ".join([f"{k} = :{k}" for k in atributos_actualizar.keys()])
    expression_attribute_values = {f":{k}": v for k, v in atributos_actualizar.items()}

    # Actualizar el ítem
    response = table.update_item(
        Key={
            'id_aerolinea': id_aerolinea
        },
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )

    return {
        'statusCode': 200,
        'body': f'Aerolínea con id_aerolinea={id_aerolinea} actualizada correctamente.'
    }
