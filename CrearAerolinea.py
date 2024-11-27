import boto3
import json

def lambda_handler(event, context):
    try:
        # Obtener los datos de la aerolínea desde el cuerpo de la solicitud
        body = json.loads(event.get('body', '{}'))  # Esto maneja el caso donde no haya un cuerpo válido

        # Verificar que los parámetros necesarios están presentes
        id_aerolinea = body.get('id_aerolinea')
        nombre = body.get('nombre')
        codigo = body.get('codigo')
        pais_origen = body.get('pais_origen')

        if not id_aerolinea or not nombre or not codigo or not pais_origen:
            raise ValueError("Faltan parámetros: id_aerolinea, nombre, codigo o pais_origen")

        # Conectar con DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Aerolíneas')

        # Crear el item de la aerolínea
        aerolinea = {
            'id_aerolinea': id_aerolinea,
            'nombre': nombre,
            'codigo': codigo,
            'pais_origen': pais_origen
        }

        # Almacenar el item en DynamoDB
        response = table.put_item(Item=aerolinea)

        # Retornar una respuesta exitosa
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Aerolínea creada con éxito'})
        }

    except ValueError as ve:
        # Captura de errores por falta de parámetros
        print(f"Error de validación: {str(ve)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(ve)})
        }

    except boto3.exceptions.Boto3Error as db_err:
        # Error relacionado con la conexión o interacción con DynamoDB
        print(f"Error de DynamoDB: {str(db_err)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error al interactuar con DynamoDB', 'details': str(db_err)})
        }

    except json.JSONDecodeError as json_err:
        # Error al procesar el JSON en el cuerpo de la solicitud
        print(f"Error al procesar JSON: {str(json_err)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Error al procesar los datos JSON', 'details': str(json_err)})
        }

    except Exception as e:
        # Captura cualquier otro tipo de error
        print(f"Error desconocido: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error', 'details': str(e)})
        }
