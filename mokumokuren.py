from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    url = 'http://192.168.0.14:7125/printer/objects/query?extruder&print_stats'
    response = requests.get(url)
    data = response.json()

    # API 応答をコンソールに出力
    print(data)

    # データを正しく渡す
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
