# from flask import Flask, render_template
# from flask_mqtt import Mqtt
# import json

# app = Flask(__name__)

# app.config['SECRET'] = 'mysecretkey'
# app.config['TEMPLATES_AUTO_RELOAD'] = True
# app.config['MQTT_BROKER_URL'] = '192.168.1.102'
# app.config['MQTT_BROKER_PORT'] =  1884
# app.config['MQTT_USERNAME'] = 'homegate'
# app.config['MQTT_PASSWORD'] =  'Homegate2021!'
# app.config['MQTT_KEEPALIVE'] = 5
# app.config['MQTT_TLS_ENABLED'] = False

# devices = ['sw0', 'sw1', 'sw2', 'sw3']

# mqtt = Mqtt(app)

# @app.route('/host')
# def dashboard():
#     return render_template('dashboard.html')

# @app.route('/')
# def settings():
#     return render_template('settings.html')

# @mqtt.on_connect()
# def handle_connect(client, userdata, flags, rc):
#     print('Connected!')
#     mqtt.subscribe('sw0')
#     for device in devices:
#         mqtt.subscribe(device)
#         print('subscribed to : ' + device)

# @mqtt.on_message()
# def handle_mqtt_message(client, userdata, message):
#     # data = dict(
#     #     topic=message.topic,
#     #     payload=message.payload.decode()
#     # )
#     topic=message.topic,
#     payload=message.payload.decode()
#     print(topic)
#     print(payload)
 

# @mqtt.on_log()
# def handle_logging(client, userdata, level, buf):
#     if level == 8:
#         print(level, buf)

# if __name__ == '__main__':
#     # app.run(debug=True, host='0.0.0.0')
#     app.run()

# main.py
import eventlet
from flask import Flask, render_template
from flask_mqtt import Mqtt
import json
from flask_socketio import SocketIO
import platform

if platform.system() == 'Darwin':
    pass
else:
    import RPi.GPIO as gpio
    gpio.setmode(gpio.BCM)
    gpio.setup(18, gpio.OUT)
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)
    gpio.setup(25, gpio.OUT)

eventlet.monkey_patch()

switch_state = {
    'sw0' : {'name': 'Device 1' ,'state': 'false'},
    'sw1' : {'name': 'Device 2' ,'state': 'false'},
    'sw2' : {'name': 'Device 3' ,'state': 'false'},
    'sw3' : {'name': 'Device 4' ,'state': 'false'}
}

pins = {
    'sw0' : {'name' : 'sw0', 'board' : 'esp8266', 'topic' : 'sw0', 'state' : 'false' },
    'sw1' : {'name' : 'sw1', 'board' : 'esp8266', 'topic' : 'sw1', 'state' : 'false' },
}

templateData = {
    'switch_state' : switch_state
}

devices = ['sw0', 'sw1', 'sw2', 'sw3']

app = Flask(__name__)
app.config['SECRET'] = 'mysecretkey'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = '192.168.1.102'
app.config['MQTT_BROKER_PORT'] =  1883
app.config['MQTT_USERNAME'] = 'home'
app.config['MQTT_PASSWORD'] =  'Home'
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)
socketio = SocketIO(app)

@app.route('/')
def dashboard():
    return render_template("dashboard.html", **templateData)

@app.route('/s')
def settings():
    return render_template("settings.html")

# @socketio.on('subscribe')
# def handle_subscribe(json_str):
#     data = json.loads(json_str)
#     mqtt.subscribe(data['topic'])

# write to RPi GPIO pins
def control_device(deviceid, status):
    if deviceid == 'sw0':
        if status == 'true':
            gpio.output(18, gpio.HIGH)
            print('[info] Device 1 is ON')
        else:
            gpio.output(18, gpio.LOW)
            print('[info] Device 1 is OFF')
    if deviceid == 'sw1':
        if status == 'true':
            gpio.output(23, gpio.HIGH)
            print('[info] Device 2 is ON')
        else:
            gpio.output(23, gpio.LOW)
            print('[info] Device 2 is OFF')
    if deviceid == 'sw2':
        if status == 'true':
            gpio.output(24, gpio.HIGH)
            print('[info] Device 3 is ON')
        else:
            gpio.output(24, gpio.LOW)
            print('[info] Device 3 is OFF')
    if deviceid == 'sw3':
        if status == 'true':
            gpio.output(25, gpio.HIGH)
            print('[info] Device 4 is ON')
        else:
            gpio.output(25, gpio.LOW)
            print('[info] Device 4 is OFF')

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    for device in devices:
        mqtt.subscribe(device)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, msg):
    if platform.system() == 'Darwin':
        print(msg.topic + " : " + msg.payload.decode())
    else:
        control_device(msg.topic, msg.payload.decode())
    # socketio.emit('mqtt_message', data)

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    if level == 8:
        print(level, buf)

if __name__ == "__main__":
    app.run(debug=True)
    #socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)
    #socketio.run(app)
