import os
import pika


# Parse SNOWBALL_URL (fallback to localhost)
url = os.environ.get('SNOWBALL_URL', 'amqp://guest:guest@localhost/snowball/%2f')

queue_params = pika.URLParameters(url)
queue_params.socket_timeout = 5


# Reset counter files
counters_path = os.path.join(os.curdir, 'counters')

if not os.path.isdir(counters_path):
    os.makedirs(counters_path)

files_list = [f for f in os.listdir(counters_path) if os.path.isfile(os.path.join(counters_path, f))]
for f in files_list:
    os.remove(os.path.join(counters_path, f))
