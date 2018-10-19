# -*- coding: utf-8 -*-

import os
import logging
import time
import serial
import requests
from random import *


#logging.basicConfig(filename=config['log_file'], level=logging.DEBUG, format='%(asctime)s %(message)s')

# count for dummy data


def loar_receiver():
    """월태그에 전달한 lora 패킷 분석"""
    #count = 0

    # UART 세팅
    ser = serial.Serial(port='/dev/ttySAC4', baudrate=115200, timeout=None)
    url = '127.0.0.1'
    while True:
        # if count == 6:
        #     count = 0
        try:
            # 샘플 데이터
            #data = 'A4FD230D3623FE81043A1E'
            # temp_data = setDummyGPS(count)
            # if type(temp_data) == tuple:
            #     count = temp_data[0]
            #     count += 1
            #     data = temp_data[1]
            # elif type(temp_data) == str:
            #     data = temp_data

            #data = setDummyGPS()
            data = ser.readline().decode('utf8').replace(' ', '').replace('\n', '')
            data = data.upper()
            print(data)
            #if not data or data[0] != 'A':
            #if not data or data[0] != 'A' or data[2:4] != 'FD':
            #    continue


            # now = time.localtime()
            # now_time = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
            #
            # web_data = "%s %s"%(now_time,data)
            # #print(web_data)
            # if data[2:4] =='FD' or data[12:14]=='FE':
            #     r = requests.post('http://%s:8008/curlc'%url, json=web_data)
            #
            # logging.info('lora: %s' % data)
        except Exception as e:
            logging.error(e, exc_info=True)
            pass

        #time.sleep(5)##########

def setDummyGPS():
    dummy_list = ['A1FD23090624FE810D0D2D','A1FD23090A1DFE810D0F31','A1FD23090D4EFE810D0E1D',
                  'A1FD23091162FE810D0C56','A1FD23091618FE810D0B0C','A1FD23091A4FFE810D0B0C']
    i = randint(0,5)
    #dummy_tuple =()
    # if count == 0:
    #     dummy_tuple =(0,dummy_list[0])
    # elif count ==1:
    #     dummy_tuple = (1, dummy_list[1])
    # elif count ==2:
    #     dummy_tuple = (2, dummy_list[2])
    # elif count ==3:
    #     dummy_tuple = (3, dummy_list[3])
    # elif count ==4:
    #     dummy_tuple = (4, dummy_list[4])
    # elif count ==5:
    #     dummy_tuple = (5, dummy_list[5])

    # return list
    return dummy_list[i]

    #return tuple
    #return dummy_tuple




if __name__ == '__main__':
    # 프로세스 아이디 저장
    # with open(config['pid_file'], "w") as f:
    #     f.write('%s' % os.getpid())

    loar_receiver()

