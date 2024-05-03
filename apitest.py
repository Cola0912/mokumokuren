import requests

response = requests.get("http://192.168.0.14:7125")
data = response.json()
print(data)