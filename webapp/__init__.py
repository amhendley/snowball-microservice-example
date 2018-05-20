import os
import pika


# Parse SNOWBALL_URL (fallback to localhost)
url = os.environ.get('SNOWBALL_URL', 'amqp://guest:guest@localhost/snowball/%2f')

queue_params = pika.URLParameters(url)
queue_params.socket_timeout = 5
