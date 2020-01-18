from bottle import Bottle, route, run, template, get, post, debug, static_file, request, redirect, response
import sys
from pathlib import Path
import os
work_dir = str(Path(os.path.realpath(__file__)).parents[1]) + "\\Code\\"
sys.path.append(work_dir)
import model
import sql_create_load
import sam_partition

@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='./static')

@route('/form')
@route('/form/')
@route('/form', method = 'POST')
@route('/form/', method = 'POST')
def index():
	return template('formExample')

@route('/formProcess')
@route('/formProcess/')
@route('/formProcess', method='POST')
@route('/formProcess/', method='POST')
def index(shock=0):
	print(request.forms.keys())
	myDict= {k:request.forms.getunicode(k) for k in request.forms.keys()}
	for(i in 1:1):
		c_shock = request.forms.get('c_shock')
		l_shock = request.forms.get('l_shock')
		model.CGE(float(c_shock), float(l_shock), 2020+i).results()

	return template('formExampleProc', shock=shock, myDict=myDict)

	
@route('/results/')
@route('/results')
#def index():
	

@route('/graph/')
@route('/graph')
def index(name="Anonymous"):
    
    
#         labels: ['Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sut', 'Sun'],
#     datasets: [{
#       label: 'apples',
#       data: [12, 19, 3, 17, 6, 3, 7],
#       backgroundColor: "rgba(153,255,51,0.4)"
#     }, {
#       label: 'oranges',
#       data: [2, 29, 5, 5, 2, 3, 10],
#       backgroundColor: "rgba(255,153,0,0.4)"
#     }]
#   }
    chartData = {
"labels":['Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sut', 'Sun'],
    "data" : {
        "apples":[12, 19, 3, 17, 6, 3, 7],
        "oranges":[2, 29, 5, 5, 2, 3, 10],
        "pears":[22, 39, 15, 16, 22, 31, 14],
    }
}
    return template('charts', name=name, chartData=chartData)

@route('/dir')
def dir():
	return (work_dir)

@route('/')
def index(name="User"):
    return template('index', message="Welcome to CGE App", loginName=name, text="This is an application made for Python and Sql course on DSBA Masters programme.")


run(host='localhost', port=8081, debug=True, reloader=True)