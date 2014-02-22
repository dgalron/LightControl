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


def send_request(opt=None):
    if opt is None:
        print 'marshalling'
        req = state.marshal()
    else:
        req = opt
    print "sending request", req, len(req)
    arduino_socket.send(req)


@app.route('/api/power', methods=['POST'])
def set_power():
    if not request.json or 'power_state' not in request.json:
        abort(400)

    state_change = request.json['power_state']
    if state_change:
        send_request()
    else:
        send_request(state.off_state)

    return jsonify(state.to_dict())


def get_new_intensity(current_value, incremental_value):
    if incremental_value > 0:
        return min(current_value + incremental_value, 255)
    elif incremental_value < 0:
        return max(current_value + incremental_value, 0)
    else:
        return current_value


@app.route('/api/dimmer/<temperature>', methods=['POST'])
def set_dimness(temperature):
    """If value is None it means change the selected temperature."""
    if not request.json or 'value' not in request.json:
        abort(400)
    incremental_value = request.json['value']
    if temperature == 'warm_white':
        state.warm = get_new_intensity(state.warm, incremental_value)
    elif temperature == 'cool_white':
        state.cool = get_new_intensity(state.cool, incremental_value)
    elif temperature == 'color':
        state.red = get_new_intensity(state.red, incremental_value)
        state.green = get_new_intensity(state.green, incremental_value)
        state.blue = get_new_intensity(state.blue, incremental_value)
    if incremental_value != 0:
        send_request()
    return jsonify(state.to_dict())


@app.route('/api/pattern', methods=['POST'])
def set_light_texture():
    if not request.json or 'texture' not in request.json:
        abort(400)
    return jsonify(state.to_dict())


@app.route('/', methods=['GET'])
def homepage():
    return render_template("default.html")


if __name__ == '__main__':
    # app.run('0.0.0.0')
    app.run('127.0.0.1', 5810)
