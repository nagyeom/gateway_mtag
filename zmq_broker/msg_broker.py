
import os
import logging
import zmq
from config import config


logging.basicConfig(filename=config['log_file'], level=logging.DEBUG,format='%(asctime)s %(message)s')

FRONTEND_POINT = 'tcp://127.0.0.1:7006'
BACKEND_POINT = 'tcp://127.0.0.1:7007'


def start_zmq_server():    
    """Binds the sockets"""
    context = zmq.Context.instance()
    context.set(zmq.MAX_SOCKETS, 100)

    frontend = context.socket(zmq.XPUB)
    frontend.bind(FRONTEND_POINT)

    backend = context.socket(zmq.XSUB)
    backend.bind(BACKEND_POINT)

    poll = zmq.Poller()
    poll.register(frontend, zmq.POLLIN)
    poll.register(backend, zmq.POLLIN)

    print('Server Started')

    while True:
        try:
            items = dict(poll.poll(1000))
            #print(items)
            if items.get(backend) == zmq.POLLIN:
                msg = backend.recv_string()
                print(msg)
                frontend.send_string(msg)
                logging.info('%s' % msg)
            elif items.get(frontend) == zmq.POLLIN:
                msg = frontend.recv_string()
                backend.send(msg)
                print('backend:',msg)
        except KeyboardInterrupt:
            break
        except:
            pass


if __name__ == '__main__':
    with open(config['pid_file'], 'w') as f:
        f.write('%s' % os.getpid())

    start_zmq_server()
