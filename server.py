from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # HTMLページを返す
    return render_template('index.html')

@app.route('/api/printer/status')
def get_printer_status():
    try:
        response = requests.get('http://192.168.0.14:7125/printer/objects/query?heater_bed&extruder')
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
