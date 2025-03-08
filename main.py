import boto3

# Configuración de clientes de AWS
s3_client = boto3.client('s3', region_name='us-east-1')
ec2_client = boto3.client('ec2', region_name='us-east-1')

# Nombre del bucket y archivo
bucket_name = 'juancito-bucket'
file_name = 'Apuesta.docx'
object_key = 'Apuesta'

# Configuración de la instancia EC2
instance_config = {
    'ImageId':
    'ami-08b5b3a93ed654d19',  # AMI de Amazon Linux 2 en us-east-1
    'InstanceType':
    't2.micro',
    'MinCount':
    1,
    'MaxCount':
    1,  # Nombre del par de claves SSH
    'SecurityGroupIds': ['sg-0e3953b123bceb276'],  # ID del grupo de seguridad
    'SubnetId':
    'subnet-0b81895bcd3d1986e',  # ID de la subred
    'TagSpecifications': [{
        'ResourceType': 'instance',
        'Tags': [{
            'Key': 'Name',
            'Value': 'juan-cardona'
        }]
    }]
}


def create_bucket():
    """Crea un bucket en S3."""
    try:
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' creado exitosamente.")
    except Exception as e:
        print(f"Error al crear el bucket: {e}")


def upload_file():
    """Sube un archivo al bucket de S3."""
    try:
        s3_client.upload_file(file_name, bucket_name, object_key)
        print(
            f"Archivo '{file_name}' subido exitosamente como '{object_key}'.")
    except Exception as e:
        print(f"Error al subir el archivo: {e}")


def create_instance():
    """Crea una instancia EC2."""
    try:
        response = ec2_client.run_instances(**instance_config)
        instance_id = response['Instances'][0]['InstanceId']
        print(f"Instancia EC2 creada con ID: {instance_id}")
        return instance_id
    except Exception as e:
        print(f"Error al crear la instancia EC2: {e}")
        return None


def main():
    """Función principal que ejecuta las acciones en secuencia."""
    # Crear el bucket
    create_bucket()

    # Subir el archivo al bucket
    upload_file()

    # Crear la instancia EC2
    create_instance()


if __name__ == "__main__":
    main()
