import os
import pika
import json
import requests
import logging


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create console handler and set level to info
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# create error file handler and set level to error
handler = logging.FileHandler(os.path.join(os.curdir, "taskrunner-error.log"), "w", encoding=None, delay="true")
handler.setLevel(logging.ERROR)
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# create debug file handler and set level to debug
handler = logging.FileHandler(os.path.join(os.curdir, "taskrunner-all.log"), "w")
handler.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Parse SNOWBALL_URL (fallback to localhost)
url = os.environ.get('SNOWBALL_URL', 'amqp://guest:guest@localhost/snowball/%2f')

queue_params = pika.URLParameters(url)

connection = pika.BlockingConnection(queue_params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='inputs', durable=True) # Declare a queue


class MsgBody(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)


def incoming_message(body):
    msg = MsgBody(body)

    logger.info('%s [%s]', msg.guid, msg.counter)

    c = int(msg.counter)
    headers = {'Content-Type': 'application/json'}
    url = 'http://localhost:9000/execute/'
    new_msg_body = {'guid': msg.guid, 'counter': (c - 1)}

    if c > 0:
        for i in range(0, c):
            resp = requests.post(url=url, headers=headers, data=new_msg_body)

            if resp.status_code >= 400:
                print(resp)


# create a function which is called on incoming messages
def callback(ch, method, properties, body):
    incoming_message(body)


# set up subscription on the queue
channel.basic_consume(callback, queue='inputs', no_ack=True)

# start consuming (blocks)
print('''TaskRunner v0.0.1 server starting up...
Listening on %s
Hit Ctrl-C to quit.
''' % url)
channel.start_consuming()

connection.close()