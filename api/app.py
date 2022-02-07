import RPi.GPIO as GPIO
from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
from datetime import datetime
import time

app = Flask(__name__)
CORS(app)

RelayPin1 = 15

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(RelayPin1, GPIO.OUT)

configurations = {
    'cms2': 100,
    'enabled': True
}

activities = []

cms2SecondsMapping = {
    '100': 12,
    '200': 24,
    '300': 36
}

@app.route('/v1/configuration', methods=['GET', 'POST'])
def configuration_call():
    if request.method == 'GET':
        return jsonify(configurations)
    if request.method == 'POST':
        request_data = request.get_json()

        configurations['cms2'] = request_data['cms2']
        configurations['enabled'] = request_data['enabled']

        return jsonify(configurations)

@app.route('/v1/activities', methods=['GET', 'POST'])
def activities_call():
    if request.method == 'GET':
        return jsonify(activities)
    if request.method == 'POST':
        request_data = request.get_json()

        type = request_data['type']
        if not type:
            return jsonify({'message': 'type not specified'}), 412

        if not configurations['enabled']:
           return jsonify({'message': 'watering disabled'}), 422

        GPIO.output(RelayPin1, GPIO.HIGH)
        time.sleep(cms2SecondsMapping[str(configurations['cms2'])])
        GPIO.output(RelayPin1, GPIO.LOW)

        now = datetime.now()

        activity = {
            'type': type,
            'value': configurations['cms2'],
            'date': now.strftime("%m/%d/%Y %H:%M:%S")
        }

        activities.append(activity)

        return jsonify(activities)
