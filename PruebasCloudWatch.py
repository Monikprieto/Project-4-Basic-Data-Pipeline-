import boto3
import time

# Conectar a CloudWatch
cloudwatch = boto3.client('logs')

log_group = 'my-log-group'
log_stream = 'my-log-stream'

# Crear el grupo y stream si no existen
def create_log_group_and_stream():
    try:
        cloudwatch.describe_log_groups(logGroupNamePrefix=log_group)
    except cloudwatch.exceptions.ResourceNotFoundException:
        cloudwatch.create_log_group(logGroupName=log_group)
        print(f"Grupo de logs '{log_group}' creado.")
    
    try:
        cloudwatch.describe_log_streams(logGroupName=log_group, logStreamNamePrefix=log_stream)
    except cloudwatch.exceptions.ResourceNotFoundException:
        cloudwatch.create_log_stream(logGroupName=log_group, logStreamName=log_stream)
        print(f"Stream de logs '{log_stream}' creado.")

# Enviar un log a CloudWatch
def send_log_to_cloudwatch(message):
    try:
        # Obtener el sequence token si es necesario
        streams = cloudwatch.describe_log_streams(
            logGroupName=log_group,
            logStreamNamePrefix=log_stream
        )
        
        sequence_token = streams['logStreams'][0].get('uploadSequenceToken', None)
        
        # Enviar log
        params = {
            'logGroupName': log_group,
            'logStreamName': log_stream,
            'logEvents': [{
                'timestamp': int(time.time() * 1000),  # Timestamp en milisegundos
                'message': message
            }]
        }

        if sequence_token:
            params['sequenceToken'] = sequence_token

        # Intentar enviar el log
        response = cloudwatch.put_log_events(**params)
        
        # Imprimir la respuesta de AWS para depuración
        print("Respuesta de AWS:", response)
        print(f"Log enviado: {message}")
        
    except Exception as e:
        print(f"Error al enviar log a CloudWatch: {e}")

# Llamar a la función para crear el grupo y el stream
create_log_group_and_stream()

# Enviar un log de prueba
send_log_to_cloudwatch("Esto es un mensaje de log de prueba.")
