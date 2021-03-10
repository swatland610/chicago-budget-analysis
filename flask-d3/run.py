from flask import Flask, jsonify, render_template
import pandas as pd
import json
# import my extract 10 year budget script
from data.extract_budget_data import Extract

app = Flask(__name__)
# this allows me to see changes I make in real time
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# pull in json data
ten_year_budgets = Extract().extract_budgets

@app.route('/')
def index():
    return render_template('analysis.html', data=ten_year_budgets)


if __name__=='__main__':
    app.run(debug=True)