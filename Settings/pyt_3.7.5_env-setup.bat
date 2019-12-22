@ECHO OFF 
TITLE Setting-up Python Enviroment
ECHO Please wait... Preparation to create new Python enviroment.
ECHO ========================================================
ECHO Creating enviroment
ECHO ========================================================
call conda create --name EnvFlume 
PAUSE
ECHO ========================================================
ECHO Installing python
ECHO ========================================================
call conda activate EnvFlume
call conda install -c conda-forge python=3.7.5
PAUSE
ECHO ========================================================
ECHO Installing packages
ECHO ========================================================
:: 
call conda install -c conda-forge numpy
::
call conda install -c conda-forge scipy
::
call conda install -c conda-forge matplotlib
::
call conda install -c conda-forge ipython
::
call conda install -c conda-forge jupyter
::
call conda install -c conda-forge jupyterlab
::
call conda install -c conda-forge pandas
::
call conda install -c conda-forge xlrd
::
call conda install -c conda-forge sympy
::
call conda install -c conda-forge nose
::
call conda install -c conda-forge requests
::
call conda install -c conda-forge Pillow
::
call conda install -c conda-forge nltk
::
call conda install -c conda-forge arrow
::
call conda install -c conda-forge wxPython
::
call conda install -c conda-forge beautifulsoup4
::
call conda install -c conda-forge statsmodels
::
call conda install -c conda-forge bokeh
::
call conda install -c conda-forge plotly
::
call conda install -c conda-forge scikit-learn
:: This package facilitates the creation and rendering of graph descriptions in the DOT language.
call conda install -c conda-forge graphviz
::
call pip install gekko
PAUSE
ECHO ========================================================
ECHO Downloading additional data
ECHO ========================================================
call python -m nltk.downloader all
PAUSE