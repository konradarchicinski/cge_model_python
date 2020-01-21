from flask import Flask, render_template, request
import sam_partition
import model
import sql_query as que
import sql_join
import pandas as pd
import datetime
import os

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/cge-results', methods=['POST', 'GET'])
def post_results():
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
                2020+i,
                page_inputs["database_name"]
            ).results()

        sql_join.join_tables(page_inputs["database_name"])

        df = que.sql_query(page_inputs["database_name"], 'CompleteResults', 'All')

        with open("_lastDBlog.txt", "w") as text_file:
            print(f"{page_inputs['database_name']} - {datetime.datetime.now()}", file=text_file)
 
    if request.method == 'GET':

        if os.path.exists("_lastDBlog.txt"):
            with open("_lastDBlog.txt", "r") as f:
                data = f.readlines()
                for line in data:
                    log_text = line.split(" - ")
            df = que.sql_query(log_text[0], 'CompleteResults', 'All')
        else: 
            df = que.sql_query("Database", 'CompleteResults', 'All')

    return render_template('/results.html', tables=[df.to_html(classes='data')])

@app.route('/chart')
def create_chart():
    return render_template('chart.html')

@app.route('/contact')
def show_contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)