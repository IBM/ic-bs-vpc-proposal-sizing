from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from appid import AppID
from utils import PROPERTIES
from volumes import *

app = Flask(__name__)
CORS(app)

appID = AppID()


def is_valid_access_token():
    if not PROPERTIES["AUTH"]:
        return True
    return appID.is_valid_access_token()


@app.route('/volumes', methods=['POST'])
@cross_origin()
def volumes():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    body = request.get_json()
    if 'tier' not in body or 'thoughput' not in body or 'iops' not in body or 'size' not in body:
        return jsonify({'error': 'Request must be JSON'}), 400
    if not is_valid_access_token():
        return jsonify({'error': 'Invalid authorization'}), 401
    return volume(body['tier']).get(body['thoughput'], body['iops'], body['size']), 200


@app.route('/token', methods=['GET'])
@cross_origin()
def token():
    valid = is_valid_access_token()
    return {"valid": valid}, 200 if valid else 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
