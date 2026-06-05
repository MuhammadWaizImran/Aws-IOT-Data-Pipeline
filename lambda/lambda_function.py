import json
import boto3
import pymysql

def get_secret():
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId='mysql-credentials')
    return json.loads(response['SecretString'])

def lambda_handler(event, context):
    secret = get_secret()

    connection = pymysql.connect(
        host=secret['host'],
        user=secret['username'],
        password=secret['password'],
        database=secret['dbname'],
        port=int(secret['port']),
        connect_timeout=5
    )

    try:
        device_id   = event.get('deviceId', 'unknown')
        temperature = event.get('temperature', 0)
        humidity    = event.get('humidity', 0)

        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sensor_data (
                    id          INT AUTO_INCREMENT PRIMARY KEY,
                    device_id   VARCHAR(50),
                    temperature FLOAT,
                    humidity    FLOAT,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute(
                "INSERT INTO sensor_data (device_id, temperature, humidity) VALUES (%s, %s, %s)",
                (device_id, temperature, humidity)
            )
        connection.commit()
        return {'statusCode': 200, 'body': 'Success'}

    finally:
        connection.close()
