import os

config = {
    'pid_file': '/var/www/p2p_server/service.pid',
    'log_file': '/var/www/p2p_server/p2p_server.log',
    'pub_topic': '1/mtag/p2p_payload',
    'serial_type': '/dev/ttySAC4',
    'zmq_broker_pub': 'tcp://127.0.0.1:7007'
}