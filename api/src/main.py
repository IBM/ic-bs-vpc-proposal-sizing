import math

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from appid import AppID
from utils import PROPERTIES
from volumes import TIERS, volume

app = Flask(__name__)
CORS(app)

appID = AppID()


def is_valid_access_token():
    if not PROPERTIES["AUTH"]:
        return True
    return appID.is_valid_access_token()


def to_positive_number(value):
    if isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number) or number <= 0:
        return None
    return number


@app.route('/volumes', methods=['POST'])
@cross_origin()
def volumes():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return jsonify({'error': 'Request must be JSON'}), 400
    if 'tier' not in body or 'thoughput' not in body or 'iops' not in body or 'size' not in body:
        return jsonify({'error': 'Request must be JSON'}), 400
    if body['tier'] not in TIERS:
        return jsonify({'error': 'Invalid tier'}), 400
    thoughput = to_positive_number(body['thoughput'])
    iops = to_positive_number(body['iops'])
    size = to_positive_number(body['size'])
    if thoughput is None or iops is None or size is None:
        return jsonify({'error': 'thoughput, iops and size must be positive numbers'}), 400
    if not is_valid_access_token():
        return jsonify({'error': 'Invalid authorization'}), 401
    return jsonify(volume(body['tier']).get(thoughput, iops, size)), 200


@app.route('/token', methods=['GET'])
@cross_origin()
def token():
    valid = is_valid_access_token()
    return {"valid": valid}, 200 if valid else 401


if __name__ == '__main__':
    app.run(host='0.0.0.0')
