from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # HTMLページを返す
    return render_template('index.html')

@app.route('/api/printer/status')
def get_printer_status():
    try:
        response = requests.get('http://192.168.0.14:7125/printer/objects/query?heater_bed&extruder&toolhead')
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/printer/home', methods=['POST'])
def home_printer():
    try:
        # KlipperのG28コマンドを送信
        url = 'http://192.168.0.14:7125/printer/gcode/script'
        payload = {'script': 'G28'}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return jsonify({"message": "Home command successful"})
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/printer/set_temperature', methods=['POST'])
def set_temperature():
    temp = request.json.get('temperature')
    try:
        # ここで実際の温度設定リクエストを送信する
        url = 'http://192.168.0.14:7125/printer/gcode/script'
        payload = {'script': f'M104 S{temp}'}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return jsonify({"message": f"Temperature set to {temp}°C"})
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
