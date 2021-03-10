from flask import Flask, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# this allows me to see changes I make in real time
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
    return render_template('analysis.html')


if __name__=='__main__':
    app.run(debug=True)