from flask import Flask, jsonify, request, abort
from flask import render_template

app = Flask(__name__)


@app.route('/api/power', methods=['POST'])
def set_power():
    if not request.json or 'power_state' not in request.json:
        abort(400)
    return jsonify({'power': request.json['power_state'], 'state_did_change': True})


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
    #app.run('0.0.0.0')
    app.run('127.0.0.1', 5810)
