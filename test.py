import shutil
import requests

#zip a folder 
folder = "Output"
shutil.make_archive(folder, 'zip', folder)

with open("Output.zip", "rb") as f:
    data = f.read()
    res = requests.post("http://192.168.1.106:5000/sendFile", files={"file": data})
    print(res.text)