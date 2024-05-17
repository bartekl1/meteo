from flask import Flask, render_template, send_file, request
import mysql.connector
import pytz
import tzlocal

import bme280
import smbus2
from w1thermsensor import W1ThermSensor
from pms5003 import PMS5003

import json
import os
import datetime
import time
import threading


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

app = Flask(__name__)

bme280_port = 1
bme280_address = 0x76

bme280_bus = None
w1_sensor = None
pms5003 = None

ds18b20_values = {
    "temperature": None
}
ds18b20_loaded = None
bme280_values = {
    "temperature": None,
    "humidity": None,
    "pressure": None
}
bme280_loaded = None
pms5003_values = {
    "pm1.0": None,
    "pm2.5": None,
    "pm10": None
}
pms5003_loaded = None

stats = None
stats_loaded = None

started = datetime.datetime.now()


def load_ds18b20():
    try:
        w1_sensor = W1ThermSensor()
    except Exception:
        w1_sensor = None
    return w1_sensor


def load_bme280():
    try:
        bme280_bus = smbus2.SMBus(bme280_port)
        bme280.load_calibration_params(bme280_bus, bme280_address)
    except Exception:
        bme280_bus = None
    return bme280_bus


def load_pms5003():
    try:
        pms5003 = PMS5003(**configs["pms5003"])
    except Exception:
        pms5003 = None
    return pms5003


def measure():
    global ds18b20_values, ds18b20_loaded, bme280_values, bme280_loaded, pms5003_values, pms5003_loaded
    ds18b20 = load_ds18b20()
    bme280_bus = load_bme280()
    pms5003 = load_pms5003()

    while True:
        try:
            ds18b20_temperature = ds18b20.get_temperature()
            ds18b20_values = {
                "temperature": ds18b20_temperature
            }
            ds18b20_loaded = datetime.datetime.now()
        except Exception:
            if ds18b20_loaded is not None and (datetime.datetime.now() - ds18b20_loaded).seconds > 60:
                ds18b20_values = {
                    "temperature": None
                }
                ds18b20_loaded = None
            if ds18b20_loaded is not None and (datetime.datetime.now() - ds18b20_loaded).seconds > 10:
                ds18b20 = load_ds18b20()
        try:
            bme280_data = bme280.sample(bme280_bus, bme280_address)
            bme280_humidity = bme280_data.humidity
            bme280_pressure = bme280_data.pressure
            bme280_temperature = bme280_data.temperature
            bme280_values = {
                "temperature": bme280_temperature,
                "humidity": bme280_humidity,
                "pressure": bme280_pressure
            }
            bme280_loaded = datetime.datetime.now()
        except Exception:
            if bme280_loaded is not None and (datetime.datetime.now() - bme280_loaded).seconds > 60:
                bme280_values = {
                    "temperature": None,
                    "humidity": None,
                    "pressure": None
                }
                bme280_loaded = None
            if bme280_loaded is not None and (datetime.datetime.now() - bme280_loaded).seconds > 10:
                bme280_bus = load_bme280()
        try:
            pms5003.reset()
            pms5003_data = pms5003.read()
            pms5003_1_0 = pms5003_data.pm_ug_per_m3(1)
            pms5003_2_5 = pms5003_data.pm_ug_per_m3(2.5)
            pms5003_10 = pms5003_data.pm_ug_per_m3(10)
            pms5003_values = {
                "pm1.0": pms5003_1_0,
                "pm2.5": pms5003_2_5,
                "pm10": pms5003_10
            }
            pms5003_loaded = datetime.datetime.now()
        except Exception:
            if pms5003_loaded is not None and (datetime.datetime.now() - pms5003_loaded).seconds > 60:
                pms5003_values = {
                    "pm1.0": None,
                    "pm2.5": None,
                    "pm10": None
                }
                pms5003_loaded = None
            if pms5003_loaded is not None and (datetime.datetime.now() - pms5003_loaded).seconds > 10:
                pms5003 = load_pms5003()
        time.sleep(2)


def load_stats():
    global stats, stats_loaded
    while True:
        try:
            tz_name = str(tzlocal.get_localzone())
            tz = pytz.timezone(tz_name)

            db = mysql.connector.connect(**configs['mysql'])
            cursor = db.cursor(dictionary=True)

            sql = 'SELECT COUNT(id) FROM readings'
            cursor.execute(sql)
            result = cursor.fetchall()
            rows_count = result[0]['COUNT(id)']

            res = {
                "status": "ok",
                "readings_count": rows_count,
            }
            check = {
                "ds18b20": {
                    "temperature": "ds18b20_temperature"
                },
                "bme280": {
                    "temperature": "bme280_temperature",
                    "humidity": "bme280_humidity",
                    "pressure": "bme280_pressure"
                },
                "pms5003": {
                    "pm1.0": "pms5003_pm_1_0",
                    "pm2.5": "pms5003_pm_2_5",
                    "pm10": "pms5003_pm_10"
                }
            }

            for sensor, values in check.items():
                res[sensor] = {}
                for key, name in values.items():
                    sql = f'SELECT id, {name}, read_time FROM readings WHERE {name} = (SELECT MIN({name}) FROM readings);'
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    dt = tz.localize(result[0]['read_time'])
                    iso = dt.isoformat()
                    date = iso
                    min_value = {
                        "id": result[0]["id"],
                        "read_time": date,
                        "value": result[0][name]
                    }

                    sql = f'SELECT id, {name}, read_time FROM readings WHERE {name} = (SELECT MAX({name}) FROM readings);'
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    dt = tz.localize(result[0]['read_time'])
                    iso = dt.isoformat()
                    date = iso
                    max_value = {
                        "id": result[0]["id"],
                        "read_time": date,
                        "value": result[0][name]
                    }

                    sql = f'SELECT AVG({name}) FROM readings'
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    avg_value = {
                        'value': int(result[0][f'AVG({name})'])
                    }

                    amp_value = {
                        'value': max_value['value'] - min_value['value']
                    }

                    res[sensor][key] = {
                        "min": min_value,
                        "max": max_value,
                        "avg": avg_value,
                        "amp": amp_value
                    }

            cursor.close()
            db.close()

            stats = res
        except Exception:
            if stats_loaded is not None and (datetime.datetime.now() - stats_loaded).seconds > 5 * 60:
                stats = None
                stats_loaded = None
                time.sleep(30)
                continue

        time.sleep(2 * 60)


@app.before_first_request
def start_threads():
    measure_thread = threading.Thread(target=measure)
    stats_thread = threading.Thread(target=load_stats)
    measure_thread.start()
    stats_thread.start()


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
    global ds18b20_values, ds18b20_loaded, bme280_values, bme280_loaded, pms5003_values, pms5003_loaded

    tz_name = str(tzlocal.get_localzone())
    tz = pytz.timezone(tz_name)
    dt = tz.localize(datetime.datetime.now())
    iso = dt.isoformat()

    ds18b20_date = tz.localize(ds18b20_loaded).isoformat() if ds18b20_loaded is not None else None
    bme280_date = tz.localize(bme280_loaded).isoformat() if bme280_loaded is not None else None
    pms5003_date = tz.localize(pms5003_loaded).isoformat() if pms5003_loaded is not None else None

    return {
        "status": "ok",
        "date": iso,
        "ds18b20": ds18b20_values,
        "bme280": bme280_values,
        "pms5003": pms5003_values,
        "ds18b20_date": ds18b20_date,
        "bme280_date": bme280_date,
        "pms5003_date": pms5003_date
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

    try:
        start_date = request.args.get('startDate')
        start_date = datetime.datetime.fromisoformat(start_date)
    except Exception:
        start_date = None
    try:
        end_date = request.args.get('endDate')
        end_date = datetime.datetime.fromisoformat(end_date)
    except Exception:
        end_date = None

    db = mysql.connector.connect(**configs['mysql'])
    cursor = db.cursor(dictionary=True)
    if start_date is None and end_date is None:
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

    else:
        if start_date is None and end_date is None:
            sql = 'SELECT * FROM readings'
            cursor.execute(sql)
        elif start_date is not None and end_date is None:
            sql = 'SELECT * FROM readings WHERE read_time >= %s'
            cursor.execute(sql, (start_date, ))
        elif start_date is None and end_date is not None:
            sql = 'SELECT * FROM readings WHERE read_time <= %s'
            cursor.execute(sql, (end_date, ))
        else:
            sql = 'SELECT * FROM readings WHERE read_time BETWEEN %s AND %s'
            cursor.execute(sql, (start_date, end_date, ))

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
def stats_api():
    global stats, started
    while stats is None and (datetime.datetime.now() - started).seconds < 60:
        time.sleep(1)
    if stats is None:
        return {"status": "error"}
    return stats


if __name__ == '__main__':
    if 'flask' in configs.keys():
        app.run(**configs['flask'])
    else:
        app.run()
