import json
import random
import time
from datetime import datetime

from flask import Flask, Response, render_template

application = Flask(__name__)
random.seed()  # Initialize the random number generator


@application.route("/")
def index():
    return render_template("index.html")


def generate_random_data():
    while True:
        json_data = json.dumps(
            {
                "time": datetime.now().strftime("%H:%M:%S"),
                "value": random.random() * 100,
            }
        )
        yield f"data:{json_data}\n\n"
        time.sleep(1)

def upper_line():
    while True:
        json_upper = json.dumps(
            {
                "time": datetime.now().strftime("%H:%M:%S"),
                "value": 90,
            })
        yield f"data:{json_upper}\n\n"
        time.sleep(1)

@application.route("/chart-data")
def chart_data():
    return Response(generate_random_data(), mimetype="text/event-stream")

@application.route("/upper-data")
def upper_data():
    return Response(upper_line(), mimetype="text/event-stream")

if __name__ == "__main__":
    application.run(debug=True)