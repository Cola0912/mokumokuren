from flask import Flask, render_template
from flask_socketio import SocketIO
import websocket
import json

app = Flask(__name__)
socketio = SocketIO(app)

# klipperのWebSocketエンドポイント
KLIPPER_WS_ENDPOINT = "ws://192.168.0.14/ws"

# WebSocket接続を開始して、データを取得する関数
def get_printer_data():
    try:
        ws = websocket.create_connection(KLIPPER_WS_ENDPOINT)
        # klipperからデータを取得
        ws.send(json.dumps({"jsonrpc": "2.0", "method": "printer.objects.query", "params": {"heaters": ["heater_bed"], "extruder": ["extruder"], "toolhead": ["toolhead"]}, "id": 0}))
        result = json.loads(ws.recv())
        ws.close()
        return result
    except Exception as e:
        print("Error:", e)
        return None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('request_printer_data')
def handle_printer_data():
    data = get_printer_data()
    if data:
        socketio.emit('printer_data', data)

if __name__ == '__main__':
    socketio.run(app)
