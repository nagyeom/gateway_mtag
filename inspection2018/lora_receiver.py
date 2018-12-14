import os
import logging
import serial
import time
import json
from random import *
from parsing_msg import MessageParser
from mqtt_simple import GatewayMQTT

logging.basicConfig(filename='/var/www/inspection2018/log_inspection.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

def lora_receiver():
    """월태그에 전달한 lora 패킷 분석"""

    # UART 세팅
    ser = serial.Serial(port='/dev/ttySAC4', baudrate=115200, timeout=None)

    # MQTT 세팅
    mqtt_client = GatewayMQTT()

    while True:
        try:
            # 샘플 데이터
            data = setDummyData()
            #data = ser.readline().decode('utf8').replace(' ', '').replace('\n', '')
            data = data.upper()

            if not data or data[0:2] != 'EF':
                continue

            print(data)
            parser = MessageParser(mqtt_client)
            result_data = parser.parseTagData(data)
            logging.info("msg type:%s result msg:%s"%(parser.msg_type, result_data))

        except Exception as e:
            logging.error(e, exc_info=True)
            pass
        #time.sleep(5)

def setDummyData():
    """
    테스트용 더미데이터
    """
    dummy_list = ['EF010143802E00016741B4000167D6B10001673CB1000167395E000167A861000167395E00011F567D0001B101F50001567D6B0064FF',
                  'EF0201448109FD230D3623FE81043A1E0064FF','EF0201448109FD23090624FE810D0D2D0064FF','EF0201448109FD23090A1DFE810D0F310064FF',
                  'EF0201448109FD23090D4EFE810D0E1D0064FF','EF0201448109FD23091162FE810D0C560064FF','EF0201448109FD23091618FE810D0B0C0064FF',
                  'EF0201448109FD23091A4FFE810D0B0C0064FF']
    i = randint(0, 1)
    return dummy_list[i]


if __name__ == '__main__':
    # 프로세스 아이디 저장
    # with open(config['pid_file'], "w") as f:
    #     f.write('%s' % os.getpid())

    lora_receiver()

