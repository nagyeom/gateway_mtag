from flask import Flask
from flask import request
import requests
import json
import os
import logging
import pymysql
import DB_func


app = Flask(__name__)
app.config['DEBUG'] = False

logging.basicConfig(filename='/var/www/gatewayToOpenCPN/gps_log.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

#dummy_count = 0
#dummy_list = []

@app.route("/", methods=['GET','POST'])
def index():
    cpn_str = None
    # global dummy_count
    if request.method == 'GET':
        db = DB_func.MySQLSet()
        sql = "SELECT * FROM gps_log ORDER BY time DESC LIMIT 10"
        log_list = db.selectGPS(sql)
        if log_list is not None:
            #cpn_str = ''.join(str(e) for e in log_list)
            #print(log_list)
            cpn_dict = {'items': log_list}
            print("index:",cpn_dict)
            logging.info('index: %s' % str(cpn_dict))

        db.closeDB()
        return json.dumps(cpn_dict)


@app.route("/curlc",methods=['GET','POST'])
def curlc():
    log_list = None
    cpn_dict = None
    #global dummy_count
    #global dummy_list
    if request.headers['Content-Type']== 'application/json':
        db = DB_func.MySQLSet()
        # print(1)
        log = request.data.decode('utf-8')
        print("curlc:",log,type(log))

        if log is not None:
            cpn_dict = parseJSON(log)
            print(cpn_dict)
            logging.info('curlc: %s' % str(cpn_dict))
            # curlc
            for item in cpn_dict['items']:
                db.insertGPS(item['tag_id'],item['lat'],item['lon'],item['time'])

            # dummy db
            # db.insertDummyGPS(dummy_list[dummy_count])
            # dummy_count += 1
            # if dummy_count == len(dummy_list):
            #     dummy_count = 0

        db.closeDB()
    return ''

def parseJSON(data):
    """
    해도 전송용 JSON 데이터로 만들기
    """
    log = data
    cpn_list = []

    #print(len(log),log)
    # for util_pkt_logger
    # time = log[0:19]
    # tag_id = log[20:22]
    #
    # # full data
    # temp_lat = log[22:32]
    # temp_lon = log[32:-1]

    # for lora_receiver
    time = log[1:20]
    tag_id = log[21:23]

    # full data
    temp_lat = log[23:33]
    temp_lon = log[33:-2]
    lat = getLatLon(temp_lat)
    lon = getLatLon(temp_lon)

    cpn_str={'tag_id':tag_id,'time':time, 'lat':lat, 'lon':lon}
    cpn_list.append(cpn_str)
    cpn_dict={'items':cpn_list}

    return cpn_dict

def getLatLon(data):
    """
    도+'.'+(분/60)+( 초.초(%100) /3600)
    """
    conversion_val = None
    name = data[0:2]
    # print(len(data))
    if name == 'FD' or name == 'FE':
        degrees = int(data[2:4],16)
        minutes = int(data[4:6],16)
        second1 = int(data[6:8],16)
        second2 = int(data[8:],16)
        seconds = str(second1)+'.'+str(second2)

        conversion_val = str(degrees+(minutes/60) + (float(seconds)/3600))

    return conversion_val

# def setDummy():
#     dummy_path = '/var/www/gatewayToOpenCPN/sample_gps_log.txt'
#     global dummy_list
#     global dummy_count
#     f = open(dummy_path, 'r')
#     while True:
#         line = f.readline().replace(';\n', '')
#         dummy_list.append(line)
#         if not line or len(line) == 0: break
#     f.close()
#     dummy_list[0] = dummy_list[0][1:]

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8008)

