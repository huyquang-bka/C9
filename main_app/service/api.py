import requests

URL = 'https://api.github.com/users/{}'
PAYLOAD = {"slot": {}, "base64": ""}

def api_send_to_web(payload):
    r = requests.post(URL, json=payload)
    try:
        return r.json()
    except:
        return None
