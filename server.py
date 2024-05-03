from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # HTMLページを返す
    return render_template('index.html')

@app.route('/api/printer/status')
def get_printer_status():
    try:
        url = 'http://192.168.0.14:7125/printer/objects/query?heater_bed&extruder&toolhead'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/printer/home', methods=['POST'])
def home_printer():
    try:
        # 以下はプリンターのAPIに合わせたURLとコマンド形式の例です
        url = 'http://192.168.0.14:7125/printer/printhead/home'
        response = requests.post(url)
        response.raise_for_status()
        return jsonify({"message": "ホームコマンド送信成功"})
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/printer/set_temperature', methods=['POST'])
def set_temperature():
    try:
        temp = request.json['temperature']
        # ここでもプリンターのAPIに合わせたリクエストを構成します
        url = f'http://192.168.0.14:7125/printer/temperature/set?target={temp}'
        response = requests.post(url)
        response.raise_for_status()
        return jsonify({"message": f"温度設定成功: {temp}℃"})
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
