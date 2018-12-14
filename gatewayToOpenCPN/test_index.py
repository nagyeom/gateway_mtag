import requests
import time
import json

while True:
    data = 'A1FD23090624FE810D0D2D'
    #r = requests.post('http://127.0.0.1:8008/curlc',json=json.dumps(data))
    r = requests.get('http://127.0.0.1:8008/')
    time.sleep(5)