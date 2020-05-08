from flask import Flask, render_template
from flask_mqtt import Mqtt
import json
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET'] = 'mysecretkey'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = '192.168.1.102'
app.config['MQTT_BROKER_PORT'] =  1884
app.config['MQTT_USERNAME'] = 'homegate'
app.config['MQTT_PASSWORD'] =  'Homegate2021!'
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)
socketio = SocketIO(app)

@app.route('/')
def dashboard():
    return render_template("dashboard.html")

@app.route('/s')
def settings():
    return render_template("settings.html")

# @socketio.on('subscribe')
# def handle_subscribe(json_str):
#     data = json.loads(json_str)
#     mqtt.subscribe(data['topic'])

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('sw0')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    socketio.emit('mqtt_message', data)

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    if level == 8:
        print(level, buf)


if __name__ == "__main__":
    #app.run(debug=True)
    socketio.run(app, host='localhost', port=5000, use_reloader=False, debug=True)
