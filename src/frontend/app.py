import os
import sys
sys.path.insert(0, os.getcwd())
from flask import Flask, redirect, url_for, render_template, request, make_response, jsonify
from src.backend.predict.realtime_predict import AudioStreamer

# Init audio streamer
AUS = AudioStreamer('config.ini')
streamer = AUS.build_streamer()


# App config
app = Flask(__name__)
app.secret_key = 'super secret key'


@app.route('/')
def index():
    labels = ["cough", "speech", "silence"]
    values = [0, 0, 0]
    return render_template('index.html', data=zip(labels, values))


@app.route("/predict", methods=['POST'])
def predict():
    # Run audio streamer
    AUS.run_streamer(streamer)
    labels = ["cough", "speech", "silence"]
    values = [0, 0, 0]
    return render_template('index.html', data=zip(labels, values))


if __name__ == '__main__':
    app.run(debug=True)
