import requests
import time

url = "http://202.191.56.104:5518/sendFile"
# url = "http://192.168.1.13:5518/sendFile"

for i in range(100):
    with open("main/C9_result.txt", "rb") as f:
        data = f.read()
        res = requests.post("http://202.191.56.104:5518/sendFile", files={"file": data})
        text = res.text
        print(text)
        if text == "Success":
            time.sleep(5)
    