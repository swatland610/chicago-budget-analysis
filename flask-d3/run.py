import os
import pandas as pd
import json
from flask import Flask, jsonify, render_template


app = Flask(__name__)
# this allows me to see changes I make in real time
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# pull in json data
JSON_PATH = os.path.join(app.static_folder, 'data', 'ten_year_budgets.json')

with open(JSON_PATH) as data:
    ten_year_budgets = json.load(data)

@app.route('/')
def index():
    return render_template('analysis.html', data=ten_year_budgets)


if __name__=='__main__':
    app.run(debug=True)
