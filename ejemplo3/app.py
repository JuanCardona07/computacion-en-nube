from flask import Flask, request, jsonify
import boto3

app = Flask(__name__)


def listar_archivos(bucket_name):
    s3 = boto3.client('s3')

    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            archivos = [obj['Key'] for obj in response['Contents']]
            return archivos
        else:
            return "El bucket está vacío o no existe."
    except Exception as e:
        return f"Error: {e}"


@app.route('/listar', methods=['GET'])
def listar():
    bucket_name = request.args.get('bucket')
    if not bucket_name:
        return jsonify({"error": "Debe proporcionar un nombre de bucket"}), 400

    archivos = listar_archivos(bucket_name)

    if isinstance(archivos, list):
        return jsonify({"archivos": archivos})
    else:
        return jsonify({"error": archivos}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
