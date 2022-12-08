from flask import Flask, request


app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World"


@app.route("/sendFile", methods=["POST"])
def send_file():
    f = request.files["file"]
    with open("Output_1.zip", "wb") as f1:
        f1.write(f.read())
    return "Success"


if __name__ == "__main__":
    app.run(host="192.168.1.106", port=5000, debug=False)