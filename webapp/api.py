import random
import string
from bottle import template, request
import logging
import os
import sys
import pika
import json
from . import queue_params, counters_path


def execute():
    guid = request.forms.get('guid')
    counter = request.forms.get('counter')

    connection = pika.BlockingConnection(queue_params)  # Connect to CloudAMQP
    channel = connection.channel()  # start a channel
    channel.queue_declare(queue='inputs', durable=True, auto_delete=False)  # Declare a queue

    # send a message
    if not guid:
        guid = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))

    body = {'guid': guid, 'counter': counter}
    channel.basic_publish(exchange='', routing_key='inputs', body=json.dumps(body))
    print("[x] Message sent to consumer")
    connection.close()

    message = {'message': 'Message sent successfully', 'content': body}
    return message


def counters():
    c = []
    
    for file in os.listdir(counters_path):
        f = open(os.path.join(counters_path, file), 'r')
        _counter = f.read()
        f.close()
        
        c.append({'guid': os.path.basename(file), 'counter': _counter})
    
    return json.dumps(c, indent=4)