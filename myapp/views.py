from myapp import app
from datetime import datetime

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/healthcheck")
def health_check():
    return {
        "status": "OK",
        "timestamp": datetime.now(),
    }
