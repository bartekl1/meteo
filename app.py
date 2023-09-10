from flask import Flask, render_template, send_file

import bme280
import smbus2
from w1thermsensor import W1ThermSensor

import json
import os

app = Flask(__name__)

bme280_port = 1
bme280_address = 0x76
bme280_bus = smbus2.SMBus(bme280_port)

bme280.load_calibration_params(bme280_bus, bme280_address)

w1_sensor = W1ThermSensor()


def load_configs(c):
    d = {}
    for key, value in c.items():
        if type(value) == str and value.startswith('$'):
            d[key] = os.environ.get(value[1:])
        elif type(value) == str and \
                (value.startswith('i$') or value.startswith('I$')):
            d[key] = int(os.environ.get(value[2:]))
        elif type(value) == dict:
            d[key] = load_configs(value)
        else:
            d[key] = value
    return d


with open('configs.json') as file:
    configs = json.load(file)
    configs = load_configs(configs)

with open('version.json') as file:
    current_version = json.load(file)['version']


@app.route('/favicon.ico')
def favicon():
    return send_file('static/img/icon.ico')


@app.route('/manifest.json')
def manifest():
    return send_file('static/manifest.json')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/current_reading')
def current_reading_api():
    bme280_data = bme280.sample(bme280_bus, bme280_address)
    bme280_humidity = bme280_data.humidity
    bme280_pressure = bme280_data.pressure
    bme280_temperature = bme280_data.temperature

    w1_temperature = w1_sensor.get_temperature()

    return {
        "bme280": {
            "temperature": bme280_temperature,
            "humidity": bme280_humidity,
            "pressure": bme280_pressure
        },
        "ds18b20": {
            "temperature": w1_temperature
        }
    }


if __name__ == '__main__':
    if 'flask' in configs.keys():
        app.run(**configs['flask'])
    else:
        app.run()
