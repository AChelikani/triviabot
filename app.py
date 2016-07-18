# Could be used as API to serve questions/other content to bot
import os
from flask import Flask, send_from_directory

app = Flask(__name__,)

@app.route("/")
def hello():
    return "Hello world!"

@app.route("/amc8/<path:path>")
def amc8(path):
    print path
    return send_from_directory("static/amc8", path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
