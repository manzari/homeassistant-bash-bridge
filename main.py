import paho.mqtt.client as mqtt
import json
import psutil
import configparser
import subprocess
import time

config = configparser.ConfigParser()
config.read('config.ini')

mqtt_client = mqtt.Client(config['device']['identifier'] + '-client')
mqtt_client.username_pw_set(username=config['broker']['username'], password=config['broker']['password'])
mqtt_client.connect(config['broker']['host'], port=int(config['broker']['port']), keepalive=60, bind_address="")


def register_sensor(attribute: str, attribute_friendly: str, device_class: str = 'None'):
    message = {
        'name': config['device']['friendly_name'] + ' ' + attribute_friendly,
        'device': {
            'identifiers': [config['device']['identifier']],
            'name': config['device']['friendly_name'],
            "model": "Homeassistant Bash Bridge",
            "manufacturer": "Manzari"
        },
        'value_template': '{{ value_json.' + attribute + ' }}',
        'device_class': device_class,
        'state_topic': config['topics']['stats'],
        'unique_id': config['device']['identifier'] + '_' + attribute
    }
    mqtt_client.publish('homeassistant/sensor/' + config['device']['identifier'] + '/' + attribute + '/config',
                        payload=json.dumps(message), qos=1,
                        retain=False)


def register_button(button: str, button_friendly: str):
    message = {
        'name': config['device']['friendly_name'] + ' ' + button_friendly,
        'device': {
            'identifiers': [config['device']['identifier']],
            'name': config['device']['friendly_name'],
            "model": "Homeassistant Bash Bridge",
            "manufacturer": "Manzari"
        },
        'unique_id': config['device']['identifier'] + '_' + button,
        'cmd_t': config['topics']['command'] + '/' + button + '/set'
    }
    mqtt_client.subscribe(config['topics']['command'] + '/' + button + '/set')
    mqtt_client.publish('homeassistant/button/' + config['device']['identifier'] + '/' + button + '/config',
                        payload=json.dumps(message), qos=1,
                        retain=False)


def publish_stats():
    message = {
        'cpu_percent': psutil.cpu_percent(1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage('/home').percent
    }
    print('publish stats', message)
    mqtt_client.publish(config['topics']['stats'], payload=json.dumps(message), qos=1,
                        retain=False)


def on_connect(client, userdata, flags, rc):
    register_sensor('cpu_percent', 'CPU', 'power_factor')
    register_sensor('memory_percent', 'Memory', 'power_factor')
    register_sensor('disk_percent', 'Disk', 'power_factor')
    for command in config['commands']:
        details = config['commands'][command].split('#')
        register_button(button_friendly=details[1], button=command)


def on_message(client, userdata, message):
    print("message:", str(message.payload.decode("utf-8")), "| topic:", message.topic)
    for command in config['commands']:
        if config['topics']['command'] + '/' + command + '/set' == message.topic:
            details = config['commands'][command].split('#')
            subprocess.run(details[0].split(' '))


mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

last = time.time()
while True:
    mqtt_client.loop()
    current = time.time()
    if current - last > int(config['device']['update_interval_seconds']):
        last = current
        publish_stats()
