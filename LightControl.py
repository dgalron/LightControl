import socket

from flask import Flask, jsonify, request, abort
from flask import render_template

from protocol import LightState

app = Flask(__name__)
app.debug = True


state = LightState()

TCP_IP = '192.168.1.3'
TCP_PORT = 1234
BUFFER_SIZE = 1024

arduino_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
arduino_socket.connect((TCP_IP, TCP_PORT))


def send_request():
    req = state.marshal()
    arduino_socket.send(req)


@app.route('/api/power', methods=['POST'])
def set_power():
    if not request.json or 'power_state' not in request.json:
        abort(400)
    state_change = state.set_power(request.json['power_state'])
    send_request()
    return jsonify({'power': request.json['power_state'], 'state_did_change': state_change})


@app.route('/api/dim', methods=['POST'])
def set_dimness():
    if not request.json or 'intensity' not in request.json:
        abort(400)
    return jsonify({'intensity': request.json['intensity'], 'state_did_change': True})


@app.route('/api/pattern', methods=['POST'])
def set_pattern():
    if not request.json or 'pattern' not in request.json:
        abort(400)
    return jsonify({'pattern': request.json['pattern'], 'state_did_change': True})


@app.route('/api/light_texture', methods=['POST'])
def set_light_texture():
    if not request.json or 'texture' not in request.json:
        abort(400)
    return jsonify({'texture': request.json['texture'], 'state_did_change': True})


@app.route('/', methods=['GET'])
def homepage():
    return render_template("default.html")


if __name__ == '__main__':
    # app.run('0.0.0.0')
    app.run('127.0.0.1', 5810)
