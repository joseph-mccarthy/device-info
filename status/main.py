
import platform
import socket
import re
import uuid
import json
import psutil
import logging
import paho.mqtt.client as paho
import os


def get_load():
    return os.getloadavg()


def get_system_info():
    try:
        info = {}
        info['platform'] = platform.system()
        info['platform-release'] = platform.release()
        info['platform-version'] = platform.version()
        info['architecture'] = platform.machine()
        info['hostname'] = socket.gethostname()
        info['ip-address'] = socket.gethostbyname(socket.gethostname())
        info['mac-address'] = ':'.join(re.findall('..',
                                       '%012x' % uuid.getnode()))
        info['processor'] = platform.processor()
        info['ram'] = str(
            round(psutil.virtual_memory().total / (1024.0 ** 3)))+" GB"
        return json.dumps(info)
    except Exception as e:
        logging.exception(e)


def send_message(payload):
    broker = "broker"
    topic = "device/status"

    client = paho.Client(client_id=payload['info']['hostname'])
    client.connect(broker)
    client.publish(topic, json.dumps(payload))

payload = json.loads(get_system_info())
load = get_load()
status = {
            "load": {
                "1":load[0],
                "5":load[1],
                "15":load[2]
            },
            "resources":{
            "disk":psutil.disk_usage("/").percent,
            "memory":psutil.virtual_memory().percent
            },
            "info":{
                "hostname":payload['hostname'],
                "address":payload['ip-address']
            }            
        }

send_message(status)
