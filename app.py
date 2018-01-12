from flask import Flask, jsonify, render_template
from redis import Redis, RedisError
import os
import socket
from engines import display_text
from engines import display_finviz
# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__, template_folder='templates')

@app.route("/")
def index():
    return render_template('layout.html',title='FUCfadsfasdfk you')
@app.route("/finviz")

def finviz():
    data = display_finviz.showLeft()
    return render_template('finviz.html', title='finviz toool', stocks=data)
@app.route("/home")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disa1bled</i>"
    data = display_text.generate_buzz()
    finviz_data = display_finviz.showLeft()
    html = "<h3>Hello this is a dockerlized FULL Continous integrated pipline</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}<b>FINALLY</b>"\
           "<br><i>message from the engine api</i> <h1> %s </h1><br> scaling..\
           systems is fun!!<br> here's a display of another engine \
           %s" % (data, jsonify(finviz_data))
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)
@app.route("/REST")
def REST():
    d = display_finviz.showLeft()
    return jsonify(d)
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=False,threaded=True)
