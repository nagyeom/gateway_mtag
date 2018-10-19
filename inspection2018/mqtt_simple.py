
import os
import logging
import json
import subprocess
import paho.mqtt.client as mqtt

logging.basicConfig(filename='/var/www/inspection2018/log_inspection.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

class MQTTClient(object):

    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        # self.client.on_message = self.on_message
        # self.client.username_pw_set(config['rel_broker_user'], password=config['rel_broker_pwd'])
        # self.client.connect_async(host=config['rel_broker_url'], port=config['rel_broker_port'])
        self.client.connect_async(host='192.168.0.2', port=1883)  # mqtt url: fs3t.iptime.org port 1883
        self.client.loop_start()
        self.is_connected = False

    def send_message(self, topic, message):
        if self.is_connected:
            result = self.client.publish(topic, message)
            # 만일 연결이 끊어졌다면 재부팅을 수행함
            logging.info('mqtt topic:%s, message:%s' % (topic, message))
            if result[0] == mqtt.MQTT_ERR_NO_CONN:
                try:
                    logging.info('network close. system rebooting')
                    subprocess.call('reboot', shell=True)
                except Exception as e:
                    logging.error(e, exc_info=True)
                    pass

    def on_connect(self, client, userdata, flags, rc):
        self.is_connected = True
        logging.info('is_connected:%s'%self.is_connected)


class GatewayMQTT():

    def __init__(self):
        self.client = MQTTClient()

    def run(self, msg):
        # scheduler = PingScheduler(client, self.gateway_id)
        # scheduler.start()

        try:
            self.client.send_message('FSRNT/Mtag', json.dumps(msg))
            logging.info('mqtt:%s'%msg)
        except Exception as e:
            logging.error(e, exc_info=True)


if __name__ == '__main__':
    mqtt_client = GatewayMQTT()
    mqtt_client.run()