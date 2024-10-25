from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/about')
def about():
    return 'About'


@app.route('/jsonify')
def jsonify():
    return jsonify({"message": "Sale not found"}), 404
