from flask import Flask
from flask import request
import requests
import json
import os
import DB_func

db = DB_func.MySQLSet()

app = Flask(__name__)
app.config['DEBUG'] = False

@app.route("/", methods=['GET','POST'])
def index():
    cpn_str = None
    if request.method == 'GET':
        log_list = db.selectTotalGPS()
        if log_list is not None:
            #cpn_str = ''.join(str(e) for e in log_list)
            #print(log_list)
            cpn_dict = {'items': log_list}
            print(type(cpn_dict))
        return json.dumps(cpn_dict)


@app.route("/curlc",methods=['GET','POST'])
def curlc():
    log_list = None
    cpn_dict = None
    if request.headers['Content-Type']== 'application/json':
        # print(1)
        log = request.data.decode('utf-8')
        #print(log,type(log))

        if log is not None:
            cpn_dict = parseJSON(log)
            #print(cpn_dict)

            for item in cpn_dict['items']:
                db.insertGPS(item['tag_id'],item['lat'],item['lon'],item['time'])
    return ''

def readPayload():
    """
    payload file을 CRC 값에 맞춰 읽어오는 함수
    """
    log_path = '/var/www/risinghf/lora_gateway/util_pkt_logger/payload.log'
    log_list =[]
    try:
        with open(log_path,'r') as f:
            log = f.readlines()
            for data in log:
                log_list.append(data[:-1])
            os.system('cat /dev/null > %s'%log_path)
    except:
        log_list = None

    return log_list


def parseJSON(data):
    """
    해도 전송용 JSON 데이터로 만들기
    """
    log = data
    cpn_list = []

    print(len(log),log)
    # for util_pkt_logger
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
    print(len(data))
    if name == 'FD' or name == 'FE':
        degrees = int(data[2:4],16)
        minutes = int(data[4:6],16)
        second1 = int(data[6:8],16)
        second2 = int(data[8:],16)
        seconds = str(second1)+'.'+str(second2)

        conversion_val = str(degrees+(minutes/60) + (float(seconds)/3600))

    return conversion_val

if __name__ == '__main__':

    app.run(host='0.0.0.0',port=8008)
