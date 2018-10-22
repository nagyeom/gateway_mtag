from flask import Flask
from flask import request
import requests
import json
import os
import logging
import zmq
from config import config



app = Flask(__name__)
app.config['DEBUG'] = False

logging.basicConfig(filename=config['log_file'], level=logging.DEBUG, format='%(asctime)s %(message)s')



#dummy_count = 0
#dummy_list = []

# @app.route("/", methods=['GET','POST'])
# def index():
#     cpn_str = None
#     # global dummy_count
#     if request.method == 'GET':
#         db = DB_func.MySQLSet()
#         sql = "SELECT * FROM gps_log ORDER BY time DESC LIMIT 10"
#         log_list = db.selectGPS(sql)
#         if log_list is not None:
#             #cpn_str = ''.join(str(e) for e in log_list)
#             #print(log_list)
#             cpn_dict = {'items': log_list}
#             #print("index:",cpn_dict)
#             #logging.info('index: %s' % str(cpn_dict))
#
#         db.closeDB()
#         return json.dumps(cpn_dict)
#

@app.route("/curlc",methods=['GET','POST'])
def curlc():
    log_list = None
    cpn_dict = None
    #global dummy_count
    #global dummy_list
    if request.headers['Content-Type']== 'application/json':
        # print(1)
        log = request.data.decode('utf-8')
        #print("curlc:",log,type(log))

        if log is not None:
            curlc_data = '%s|%s' % (topic, log)
            socket.send(curlc_data.encode('ascii'))
            logging.info(curlc_data.encode('ascii'))
    return ''


if __name__ == '__main__':
    with open(config['pid_file'], "w") as f:
        f.write('%s' % os.getpid())
    # zeromq broker 연결
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.connect(config['zmq_broker_pub'])
    topic = config['pub_topic']

    app.run(host='0.0.0.0',port=8008)
