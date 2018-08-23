# -*- coding: utf-8 -*-

import os

config = {
    'pid_file': '/var/www/gateway_lora_service/service.pid',
    'log_file': '/var/www/gateway_lora_service/lora_service.log',
    'pub_topic': '1/hospital/lora_msg',
    'serial_type': '/dev/ttySAC4',
    'zmq_broker_pub': os.environ.get('ZMQBROKER_PUB')
}