from flask import Flask
from redis import Redis, RedisError
import os
import socket
from engines import display_text

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cfadsannot connect to Redis, counter disa1bled</i>"
    data = display_text.generate_buzz()
    html = "<h3>Hello BOOOOB{name}! VERSION 5</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"\
           "DATA: <h1> %s </h1>" % data
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)

if __name__ == "__main__":
    app.run(host='0.0.0.0',threaded=True)
