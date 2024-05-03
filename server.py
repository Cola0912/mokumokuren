from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

PRINTER_URL = "http://192.168.0.14:7125"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/printer/status')
def get_printer_status():
    response = requests.get(f"{PRINTER_URL}/printer/objects/query?extruder&print_stats")
    data = response.json()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
