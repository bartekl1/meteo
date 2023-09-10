import requests
import mysql.connector

import json
import os


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


def main():
    if 'flask' in configs.keys() and 'port' in configs['flask'].keys():
        http_port = configs['flask']['port']
    else:
        http_port = 5000

    r = requests.get(f'http://localhost:{http_port}/api/current_reading')
    rj = r.json()

    bme280_temperature = rj['bme280']['temperature']
    bme280_humidity = rj['bme280']['humidity']
    bme280_pressure = rj['bme280']['pressure']

    ds18b20_temperature = rj['ds18b20']['temperature']

    db = mysql.connector.connect(**configs['mysql'])
    cursor = db.cursor()
    sql = 'INSERT INTO readings (bme280_temperature, bme280_humidity, bme280_pressure, ds18b20_temperature) VALUES (%s, %s, %s, %s)'
    cursor.execute(sql, (bme280_temperature,
                         bme280_humidity,
                         bme280_pressure,
                         ds18b20_temperature))
    db.commit()
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
