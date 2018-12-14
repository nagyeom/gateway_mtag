import paho.mqtt.client as mqtt
import logging
import datetime
import os
import json
import subprocess



class MQTTClient(object):

    def __init__(self,ip,port,pload_func,pub_topic=None,sub_topic=None):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.sub_topic=sub_topic
        #self.client.username_pw_set(config['rel_broker_user'], password=config['rel_broker_pwd'])
        self.client.connect_async(host=ip, port=1883)
        # self.client.connect_async(host=config['dev_broker_url'])
        # self.client.connect_async(host='fs3t.iptime.org',port=1883)
        self.client.loop_start()
        self.is_connected = False
        self.sub_msg = None
        self.pload_func=pload_func
        self.now_time = None


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


    def on_message(self, client, userdata, msg):
        try:
            self.sub_msg=msg.payload
            time_temp = str(datetime.datetime.now())
            #현재시간과 저장해둔 시간을 비교해서 같으면
            if self.now_time != time_temp:
                self.pload_func(self.sub_msg,time_temp)
                self.now_time = time_temp
        except Exception as e:
            logging.error(e, exc_info=True)

    def on_publish(self, client, userdata, mid):
        print('published')