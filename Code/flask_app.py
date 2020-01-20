#from flask import Flask, render_template, request
import sam_partition
import model

from flask import Flask, request, render_template, session, redirect
import numpy as np
import pandas as pd

app = Flask(__name__)

@app.route('/')
def hello(name=None):
    return render_template('index.html', name=name)

df = pd.DataFrame({'A': [0, 1, 2, 3, 4],
                   'B': [5, 6, 7, 8, 9],
                   'C': ['a', 'b', 'c--', 'd', 'e']})

@app.route('/cge-results', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        page_inputs = {k: request.form.get(k) for k in request.form.keys()}
        
        sam_partition.sam_data_preparation(
            page_inputs["file_name"], 
            page_inputs["sheet_name"], 
            page_inputs["setting_name"]
        )
        for i in range(5):
            model.CGE(
                float(page_inputs[f"cap_shock_{2020 + i}"]), 
                float(page_inputs[f"lab_shock_{2020 + i}"]),
                page_inputs["file_name"], 
                2020+i
            ).results()
    return render_template('/results.html', tables=[df.to_html(classes='data')], titles=df.columns.values)

if __name__ == '__main__':
    app.run(host='127.0.0.1')