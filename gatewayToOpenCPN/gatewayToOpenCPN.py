
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import json
import cgi
import random
import logging

logging.basicConfig(filename='mtag_openCPN.log', level=logging.DEBUG,format='%(asctime)s %(message)s')

class Server(BaseHTTPRequestHandler):
    id = []
    lat = []
    lon = []

    # def __init__(self,isDemo = False, size = 0) :
    #     if isDemo :
    #         self.random_arr(size)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def random_arr(self,size) :
        id_name = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth']
        del self.id[:]
        del self.lat[:]
        del self.lon[:]
        for gen in range(0, size) : 
            rand_lat = round(random.uniform(34.9, 35.2),6)
            rand_lon = round(random.uniform(128.9, 129.1),6)
            self.id.append(id_name[gen])
            self.lat.append(rand_lat) 
            self.lon.append(rand_lon)
        
    def do_HEAD(self):
        self._set_headers()
        
    def makeJson(self, id, lat, lon) :
        self.random_arr(10)                 #Demo - random generate arr : id, lat, lon
        string_info = '{ "items" : [{ '
        for order in range(0,len(id)):
            string_info += '"name" : "'
            string_info += str(id[order])
            string_info += '", "lat" : '
            string_info += str(lat[order])
            string_info += ', "lon" : '
            string_info += str(lon[order])
            if not order == len(id)-1 : 
                string_info += '}, { '
            else :
                string_info += '} '
        string_info += ']}'
        logging.info('summary: %s' % string_info)
        return string_info

    
    # GET sends back a Hello world message
    def do_GET(self):
        self._set_headers()
        # self.wfile.write(self.makeJson(id, lat, lon))
        self.wfile.write(self.makeJson(self.id,self.lat,self.lon))
        
    # POST echoes the message adding a JSON field
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return
            
        # read the message and convert it into a python dictionary
        length = int(self.headers.getheader('content-length'))
        message = json.loads(self.rfile.read(length))
        
        # add a property to the object, just to mess with data
        message['received'] = 'ok'
        
        # send the message back
        self._set_headers()
        self.wfile.write(json.dumps(message))
        
def run(server_class=HTTPServer, handler_class=Server, port=8008):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    print 'Starting httpd on port %d...' % port
    httpd.serve_forever()
    
if __name__ == "__main__":
    from sys import argv
    
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
