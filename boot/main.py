import json
import paho.mqtt.client as paho
import platform
import socket
import uuid
import psutil
import logging
import re


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def get_system_info():
    try:
        info = {}
        info['platform'] = platform.system()
        info['platform-release'] = platform.release()
        info['platform-version'] = platform.version()
        info['architecture'] = platform.machine()
        info['hostname'] = socket.gethostname()
        info['ip-address'] = get_ip_address()
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
    topic = "device/boot"

    client = paho.Client(client_id=payload['hostname'])
    client.connect(broker)
    client.publish(topic, json.dumps(payload))


payload = json.loads(get_system_info())
send_message(payload)
