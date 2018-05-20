import os
import logging


def incoming_message(body):
    print(body)


def failed_message(body):
    print('Failed: %s' % body)
