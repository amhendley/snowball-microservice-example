from bottle import Bottle
from webapp import api


web_app = Bottle()

web_app.route('/execute/', method='POST', callback=api.execute)
web_app.route('/counters/', method='GET', callback=api.counters)
