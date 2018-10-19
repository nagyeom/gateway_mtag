import re
import requests
import time
import json
import logging
from ctypes import c_int8
from mqtt_simple import GatewayMQTT


logging.basicConfig(filename='/var/www/inspection2018/log_inspection.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

class MessageParser():
    def __init__(self,mqtt_client):
        self.result_data = {}
        self.msg_type = ''
        self.mqtt_client = mqtt_client

    def parseTagData(self,packet):
        packet_list = self.slicePacket(packet)

        self.setTagID(packet_list)
        self.setMSGType(packet_list)
        self.setEmergency(packet_list)
        self.parseData(packet_list)

        self.batteryRemain(packet_list)

        return self.result_data

    def slicePacket(self, packet):
        return re.compile('(..)').findall(packet)

    def setTagID(self,packet_list):
        """
        tag id 01:승선자용태그 02:선원용스마트밴드 03:화물용태그
        """
        tag_id="".join(packet_list[2:4])
        if packet_list[2] == '01':
            tag_type="passenger"
        elif packet_list[2] == '02':
            tag_type="sailor"
        elif packet_list[2] == '03':
            tag_type="freight"
        else :
            tag_type = None

        self.result_data.update({"tag_id":tag_id,"tag_type":tag_type})

    def setMSGType(self,packet_list):
        """
        msg type 80:선내데이터(비콘) 81:선외데이터(GPS)
        """
        temp_msg = packet_list[4]
        if temp_msg == "80":
            self.msg_type = "beacon"
        elif temp_msg == "81":
            self.msg_type = "GPS"


    def parseData(self, packet_list):
        """
        msg type에 따라 length값 뒤에 붙는 message data를 파싱한다.
        """
        msg_type = packet_list[4]
        msg_length = int(packet_list[5],16)
        if msg_type == '80': #선내 데이터
            self.countBeacon(packet_list,msg_length)
            #mqtt
            #print("result_data : %s"%self.result_data)

            self.mqtt_client.run(json.dumps(self.result_data))
            logging.info("mqtt : %s"%json.dumps(self.result_data))
        elif msg_type == "81":
            self.setGPStoDB(packet_list)


    def countBeacon(self,packet_list,msg_length):
        """
        수신한 비콘 리스트의 가장 첫번째 비콘 데이터를 추출한다.
        """
        beacon_id = None
        bcRSSI = None
        if msg_length >= 7:
            bcMajor = "".join(packet_list[6:8])
            bcMinor = int("".join(packet_list[8:10]), 16)
            beacon_id="%s%d" % (bcMajor, bcMinor)

            tmpRssi = int(packet_list[10], 16)
            bcRSSI = c_int8(tmpRssi).value

        self.result_data.update({"beacon_id":beacon_id,"rssi":bcRSSI})


    def setGPStoDB(self,packet_list):
        """
        GPS 데이터를 DB에 저장한다.
        """
        now = time.localtime()
        now_time = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

        data=self.result_data["tag_id"]+"".join(packet_list[6:16])
        web_data = "%s %s" % (now_time, data)
        # print(web_data)

        r = requests.post('http://127.0.0.1:8008/curlc', json=web_data)
        self.result_data.update({'web': web_data})

    def setEmergency(self,packet_list):
        """
        emergency status 파싱
        """
        emer_status = packet_list[-3]
        self.result_data.update({"emergency":emer_status})

    def batteryRemain(self,packet_list):
        """
        잔여 배터리 용량 파싱
        """
        battery_remain = int(packet_list[-2],16)
        self.result_data.update({"ba":battery_remain})


