from flask import Flask

import json

app = Flask(__name__)


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

if __name__ == '__main__':
    if 'flask' in configs.keys():
        app.run(**configs['flask'])
    else:
        app.run()
