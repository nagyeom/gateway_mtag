import os

config = {
    'pid_file': '/var/www/p2p_program/p2p_server/service.pid',
    'log_file': '/var/www/p2p_program/p2p_server/p2p_server.log',
    'pub_topic': 'mtag/p2p_payload',
    'serial_type': '/dev/ttySAC4',
    'zmq_broker_pub': 'tcp://localhost:7007',
    #FRONTEND_POINT = 'tcp://127.0.0.1:7006'
    #BACKEND_POINT = 'tcp://127.0.0.1:7007'

    # ZMQBROKER_PUB=tcp://localhost:7007
    # ZMQBROKER_SUB=tcp://localhost:7006
    'mqtt_ip':'127.0.0.1',
    'mqtt_port' : 1883
}