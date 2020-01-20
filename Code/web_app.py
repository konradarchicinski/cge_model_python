from bottle import route, run, template, request, TEMPLATE_PATH
from pathlib import Path
import os
import sam_partition
import model

work_dir = str(Path(os.path.realpath(__file__)).parents[1])
TEMPLATE_PATH.insert(0, work_dir + '\\Code\\views')

@route('/')
def index(name="Anonymous"):
    return template('index', name=name)

@route('/cge-results', method='POST')
@route('/xge-results/', method='POST')
def index(name="Anonymous"):
    print(request.forms.keys())
    myDict = {k: request.forms.getunicode(k) for k in request.forms.keys()}
    
    sam_partition.sam_data_preparation(
        myDict["file_name"], myDict["sheet_name"], myDict["setting_name"]
    )
    for i in range(5):
        model.CGE(
            float(myDict[f"cap_shock_{2020 + i}"]), 
            float(myDict[f"lab_shock_{2020 + i}"]),
            myDict["file_name"], 
            2020+i
        ).results()
    return template('results', name=name, myDict=myDict)

@route('/charts/')
@route('/charts')
def index(name="Anonymous"):

    chartData = {
"labels":['Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sut', 'Sun'],
    "data" : {
        "apples":[12, 19, 3, 17, 6, 3, 7],
        "oranges":[2, 29, 5, 5, 2, 3, 10],
        "pears":[22, 39, 15, 16, 22, 31, 14],
    }
}
    return template('charts', name=name, chartData=chartData)

run(host='localhost', port=8080, debug=True, reloader=True)