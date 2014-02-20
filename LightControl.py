import struct
import socket

from flask import Flask, jsonify, request, abort
from flask import render_template

app = Flask(__name__)


class BitVector64(object):
    def __init__(self, val=0):
        self.__bit_vector = ''.join(['0' for _ in xrange(64)])
        self.set_bits(0, val)

    def get_bits(self, start, end):
        return self.__bit_vector[start:end]

    def set_bits(self, location, value):
        assert type(value) == int
        s = '{0:b}'.format(value)
        self.__bit_vector = self.__bit_vector[:location] + s + self.__bit_vector[location + len(s):]
        assert len(self.__bit_vector) == 64

    def bitwise_and(self, other):
        assert len(other.__bit_vector) == 64
        r = ['1' if int(i) + int(j) == 2 else '0' for i, j in zip(self.__bit_vector, other.__bit_vector)]
        assert len(r) == 64
        return r

    def __str__(self):
        return self.__bit_vector

    def __int__(self):
        return int(self.__bit_vector, 2)


# TODO: Make this a singleton
class LightState(object):
    def __init__(self):
        self.power = BitVector64(0)
        self.white = BitVector64(0)
        self.white_texture = BitVector64(0)
        self.white_dimness = BitVector64(0)
        self.color = BitVector64(0)
        self.red_val = BitVector64(0)
        self.green_val = BitVector64(0)
        self.blue_val = BitVector64(0)
        self.color_pattern = BitVector64(0)

    def set_power(self, val):
        prev_val = int(self.power.get_bits(0, 1))
        self.power.set_bits(0, val)
        return prev_val != val

    def set_white(self, val):
        pass

    def set_dimness(self, val):
        pass

    def set_color_pattern(self, val):
        pass

    def set_white_texture(self, val):
        pass

    def marshal(self):
        print 'in marshal', str(self)
        p = int(self.power) | int(self.white) | int(self.white_texture) | int(self.white_dimness)
        print 'got p', p
        p = p | int(self.color) | int(self.red_val) | int(self.green_val) | int(self.blue_val) | int(self.color_pattern)
        print 'got p finally', p, type(p)
        return struct.pack('L', p)

    def __str__(self):
        return '{0} {1} {2} {3} {4} {5} {6} {7} {8}' \
            .format(self.power, self.white, self.white_texture, self.white_dimness, self.color, self.red_val,
                    self.green_val, self.blue_val, self.color_pattern)

state = LightState()

TCP_IP = '192.168.1.3'
TCP_PORT = 1234
BUFFER_SIZE = 1024

arduino_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
arduino_socket.connect((TCP_IP, TCP_PORT))


def send_request():
    print 'in send_request', state.power
    req = state.marshal()
    print 'marshalled request', req
    arduino_socket.send(req)
    print 'sent to arduino'


@app.route('/api/power', methods=['POST'])
def set_power():
    if not request.json or 'power_state' not in request.json:
        abort(400)
    print 'received request', request.json
    state_change = state.set_power(request.json['power_state'])
    print 'state change', state_change
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

app.debug = True

if __name__ == '__main__':
    #app.run('0.0.0.0')
    app.run('127.0.0.1', 5810)
