from flask import Flask, render_template, request
import sam_partition
import model
import sql_query as que
import sql_join
import pandas as pd

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

@app.route('/')
def hello(name=None):
    return render_template('index_new.html', name=name)

@app.route('/cge-results', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        page_inputs = {k: request.form.get(k) for k in request.form.keys()}
        
        sam_partition.sam_data_preparation(
            page_inputs["file_name"], 
            page_inputs["setting_name"]
        )
        for i in range(5):
            model.CGE(
                float(page_inputs[f"cap_shock_{2020 + i}"]), 
                float(page_inputs[f"lab_shock_{2020 + i}"]),
                page_inputs["file_name"], 
                2020+i
            ).results()

        sql_join.join_tables(page_inputs["database_name"])

        df = que.sql_query(page_inputs["database_name"], 'CompleteResults', 'All')

    return render_template('/results_new.html', tables=[df.to_html(classes='data')])

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)