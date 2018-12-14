import paho.mqtt.client as mqtt
import logging
import os
import json
import subprocess


class MQTTClient(object):

    def __init__(self,ip,port,pub_topic=None,sub_topic=None ):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        #self.client.username_pw_set(config['rel_broker_user'], password=config['rel_broker_pwd'])
        self.client.connect_async(host=ip, port=1883)
        # self.client.connect_async(host=config['dev_broker_url'])
        # self.client.connect_async(host='fs3t.iptime.org',port=1883)
        self.client.loop_start()
        self.is_connected = False
        self.sub_msg = None



    def send_message(self, topic, message):
        if self.is_connected:
            result = self.client.publish(topic, message)
            # 만일 연결이 끊어졌다면 재부팅을 수행함
            if result[0] == mqtt.MQTT_ERR_NO_CONN:
                try:
                    logging.info('network close. system rebooting')
                    subprocess.call('reboot', shell=True)
                except:
                    pass

    def on_connect(self, client, userdata, flags, rc):
        if self.sub_topic:
            self.client.subscribe(self.sub_topic)
        self.is_connected = True


    def on_publish(self, client, userdata, mid):
        print('published')