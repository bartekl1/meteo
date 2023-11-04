from flask import Flask, render_template, send_file, request
import mysql.connector
import pytz
import tzlocal

import bme280
import smbus2
from w1thermsensor import W1ThermSensor

import json
import os

app = Flask(__name__)

bme280_port = 1
bme280_address = 0x76

bme280_bus = None
w1_sensor = None

def load_sensors():
    global bme280_bus, w1_sensor

    bme280_bus = smbus2.SMBus(bme280_port)

    bme280.load_calibration_params(bme280_bus, bme280_address)

    w1_sensor = W1ThermSensor()


try:
    load_sensors()
except Exception:
    pass


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


@app.route('/manifest_pl.json')
def manifest_pl():
    return send_file('static/manifest_pl.json')


@app.route('/')
def index():
    return render_template('index.html', version=current_version)


@app.route('/api/current_reading')
def current_reading_api():
    if bme280_bus == None or w1_sensor == None:
        try:
            load_sensors()
        except Exception:
            return {
                "status": "error",
                "error": "sensor_error"
            }

    try:
        bme280_data = bme280.sample(bme280_bus, bme280_address)
        bme280_humidity = bme280_data.humidity
        bme280_pressure = bme280_data.pressure
        bme280_temperature = bme280_data.temperature

        w1_temperature = w1_sensor.get_temperature()

        return {
            "status": "ok",
            "bme280": {
                "temperature": bme280_temperature,
                "humidity": bme280_humidity,
                "pressure": bme280_pressure
            },
            "ds18b20": {
                "temperature": w1_temperature
            }
        }
    
    except Exception:
        return {
            "status": "error",
            "error": "sensor_error"
        }


@app.route('/api/archive_readings/count')
def count_archive_readings_api():
    db = mysql.connector.connect(**configs['mysql'])
    cursor = db.cursor()
    sql = 'SELECT COUNT(id) FROM readings'
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()

    return {'rows_count': result[0][0]}


@app.route('/api/archive_readings')
def archive_readings_api():
    start_id = request.args.get('startId')
    try:
        limit = int(request.args.get('limit'))
    except Exception:
        limit = None
    # reverse_direction = request.args.get('reverseDirection') == "true"

    db = mysql.connector.connect(**configs['mysql'])
    cursor = db.cursor(dictionary=True)
    if start_id is None and limit is None:
        sql = 'SELECT * FROM readings'
        # if reverse_direction:
        #     sql += ' ORDER BY id DESC'
        cursor.execute(sql)
    elif start_id is not None and limit is None:
        sql = 'SELECT * FROM readings WHERE id >= %s'
        # if reverse_direction:
        #     sql += ' ORDER BY id DESC'
        cursor.execute(sql, (start_id, ))
    elif start_id is None and limit is not None:
        sql = 'SELECT * FROM readings LIMIT %s'
        # if reverse_direction:
        #     sql = 'SELECT * FROM readings ORDER BY id DESC LIMIT %s'
        cursor.execute(sql, (limit, ))
    else:
        sql = 'SELECT * FROM readings WHERE id >= %s LIMIT %s'
        # if reverse_direction:
        #     sql = 'SELECT * FROM readings WHERE id >= %s ORDER BY id DESC LIMIT %s'
        cursor.execute(sql, (start_id, limit))
    result = cursor.fetchall()
    cursor.close()
    db.close()

    tz_name = str(tzlocal.get_localzone())
    tz = pytz.timezone(tz_name)
    for i in range(len(result)):
        dt = tz.localize(result[i]['read_time'])
        iso = dt.isoformat()
        result[i]['read_time'] = iso

    return json.dumps(result)


@app.route('/api/stats')
def stats():
    tz_name = str(tzlocal.get_localzone())
    tz = pytz.timezone(tz_name)

    db = mysql.connector.connect(**configs['mysql'])
    cursor = db.cursor(dictionary=True)

    sql = 'SELECT COUNT(id) FROM readings'
    cursor.execute(sql)
    result = cursor.fetchall()
    rows_count = result[0]['COUNT(id)']

    sql = 'SELECT id, bme280_temperature, read_time FROM readings WHERE bme280_temperature = (SELECT MIN(bme280_temperature) FROM readings);'
    cursor.execute(sql)
    result = cursor.fetchall()
    dt = tz.localize(result[0]['read_time'])
    iso = dt.isoformat()
    date = iso
    min_bme280_temperature = {
        "id": result[0]["id"],
        "read_time": date,
        "value": result[0]["bme280_temperature"]
    }

    sql = 'SELECT id, bme280_temperature, read_time FROM readings WHERE bme280_temperature = (SELECT MAX(bme280_temperature) FROM readings);'
    cursor.execute(sql)
    result = cursor.fetchall()
    dt = tz.localize(result[0]['read_time'])
    iso = dt.isoformat()
    date = iso
    max_bme280_temperature = {
        "id": result[0]["id"],
        "read_time": date,
        "value": result[0]["bme280_temperature"]
    }

    sql = 'SELECT AVG(bme280_temperature) FROM readings'
    cursor.execute(sql)
    result = cursor.fetchall()
    avg_bme280_temperature = {
        'value': result[0]['AVG(bme280_temperature)']
    }

    amp_bme280_temperature = {
        'value': max_bme280_temperature['value'] - min_bme280_temperature['value']
    }

    sql = 'SELECT id, bme280_humidity, read_time FROM readings WHERE bme280_humidity = (SELECT MIN(bme280_humidity) FROM readings);'
    cursor.execute(sql)
    result = cursor.fetchall()
    dt = tz.localize(result[0]['read_time'])
    iso = dt.isoformat()
    date = iso
    min_bme280_humidity = {
        "id": result[0]["id"],
        "read_time": date,
        "value": result[0]["bme280_humidity"]
    }

    sql = 'SELECT id, bme280_humidity, read_time FROM readings WHERE bme280_humidity = (SELECT MAX(bme280_humidity) FROM readings);'
    cursor.execute(sql)
    result = cursor.fetchall()
    dt = tz.localize(result[0]['read_time'])
    iso = dt.isoformat()
    date = iso
    max_bme280_humidity = {
        "id": result[0]["id"],
        "read_time": date,
        "value": result[0]["bme280_humidity"]
    }

    sql = 'SELECT AVG(bme280_humidity) FROM readings'
    cursor.execute(sql)
    result = cursor.fetchall()
    avg_bme280_humidity = {
        'value': result[0]['AVG(bme280_humidity)']
    }

    amp_bme280_humidity = {
        'value': max_bme280_humidity['value'] - min_bme280_humidity['value']
    }

    sql = 'SELECT id, bme280_pressure, read_time FROM readings WHERE bme280_pressure = (SELECT MIN(bme280_pressure) FROM readings);'
    cursor.execute(sql)
    result = cursor.fetchall()
    dt = tz.localize(result[0]['read_time'])
    iso = dt.isoformat()
    date = iso
    min_bme280_pressure = {
        "id": result[0]["id"],
        "read_time": date,
        "value": result[0]["bme280_pressure"]
    }

    sql = 'SELECT id, bme280_pressure, read_time FROM readings WHERE bme280_pressure = (SELECT MAX(bme280_pressure) FROM readings);'
    cursor.execute(sql)
    result = cursor.fetchall()
    dt = tz.localize(result[0]['read_time'])
    iso = dt.isoformat()
    date = iso
    max_bme280_pressure = {
        "id": result[0]["id"],
        "read_time": date,
        "value": result[0]["bme280_pressure"]
    }

    sql = 'SELECT AVG(bme280_pressure) FROM readings'
    cursor.execute(sql)
    result = cursor.fetchall()
    avg_bme280_pressure = {
        'value': result[0]['AVG(bme280_pressure)']
    }

    amp_bme280_pressure = {
        'value': max_bme280_pressure['value'] - min_bme280_pressure['value']
    }

    sql = 'SELECT id, ds18b20_temperature, read_time FROM readings WHERE ds18b20_temperature = (SELECT MIN(ds18b20_temperature) FROM readings);'
    cursor.execute(sql)
    result = cursor.fetchall()
    dt = tz.localize(result[0]['read_time'])
    iso = dt.isoformat()
    date = iso
    min_ds18b20_temperature = {
        "id": result[0]["id"],
        "read_time": date,
        "value": result[0]["ds18b20_temperature"]
    }

    sql = 'SELECT id, ds18b20_temperature, read_time FROM readings WHERE ds18b20_temperature = (SELECT MAX(ds18b20_temperature) FROM readings);'
    cursor.execute(sql)
    result = cursor.fetchall()
    dt = tz.localize(result[0]['read_time'])
    iso = dt.isoformat()
    date = iso
    max_ds18b20_temperature = {
        "id": result[0]["id"],
        "read_time": date,
        "value": result[0]["ds18b20_temperature"]
    }

    sql = 'SELECT AVG(ds18b20_temperature) FROM readings'
    cursor.execute(sql)
    result = cursor.fetchall()
    avg_ds18b20_temperature = {
        'value': result[0]['AVG(ds18b20_temperature)']
    }

    amp_ds18b20_temperature = {
        'value': max_ds18b20_temperature['value'] - min_ds18b20_temperature['value']
    }

    cursor.close()
    db.close()

    return {
        "readings_count": rows_count,
        "bme280": {
            "temperature": {
                "min": min_bme280_temperature,
                "max": max_bme280_temperature,
                "avg": avg_bme280_temperature,
                "amp": amp_bme280_temperature
            },
            "humidity": {
                "min": min_bme280_humidity,
                "max": max_bme280_humidity,
                "avg": avg_bme280_humidity,
                "amp": amp_bme280_humidity
            },
            "pressure": {
                "min": min_bme280_pressure,
                "max": max_bme280_pressure,
                "avg": avg_bme280_pressure,
                "amp": amp_bme280_pressure
            }
        },
        "ds18b20": {
            "temperature": {
                "min": min_ds18b20_temperature,
                "max": max_ds18b20_temperature,
                "avg": avg_ds18b20_temperature,
                "amp": amp_ds18b20_temperature
            }
        }
    }

if __name__ == '__main__':
    if 'flask' in configs.keys():
        app.run(**configs['flask'])
    else:
        app.run()
