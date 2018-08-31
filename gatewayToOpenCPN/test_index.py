import requests
import time

while True:
    r = requests.get('http://192.168.0.21:8008/')
    print(r.text)

    time.sleep(10)