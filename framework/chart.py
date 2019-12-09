import plotly as py
import plotly.graph_objs as go
import ipywidgets as widgets
import numpy as np
from scipy import special
##########################################################################
import warnings
warnings.filterwarnings('ignore')
##########################################################################

py.offline.init_notebook_mode(connected=True)

X1, X2 = np.meshgrid(np.linspace(0, 10, 100), np.linspace(0, 10, 100))
layout = go.Layout(
    title='Constant elasticity of substitution (CES) Utility Function',
    autosize=True,
    height=800,
    scene={
        "xaxis": {
            'title': "Quantity of X1",
            "tickfont": {
                "size": 10}},
        "yaxis": {
            "title": "Quantity of X2",
            "tickfont": {
                "size": 10}},
        "zaxis": {
            "title": "Utility value",
            "tickfont": {
                "size": 10}},
        "camera": {
            "eye": {
                "x": -1.5,
                "y": -1.5,
                "z": 0.5}}})


def update_plot(sigma, a_x, a_y, A):
    def prod_fun(X, Y):
        return A * (((a_x * X)**(1 / sigma))**(sigma - 1) + \
                    ((a_y * Y)**(1 / sigma))**(sigma - 1))**(sigma / (sigma - 1))

    surface = go.Surface(
        x=X1,
        y=X2,
        z=prod_fun(
            X1,
            X2),
        colorscale="Blues",
        colorbar={
            "title": "Function value",
            "len": 1.0,
            "thickness": 20})
    fig = go.Figure(data=surface, layout=layout)
    fig.update_traces(
        contours_z=dict(
            show=True,
            usecolormap=False,
            project_z=True))

    py.offline.iplot(fig)


##########################################################################
sigma = widgets.BoundedFloatText(
    value=0.5,
    min=-100,
    max=100,
    step=0.05,
    description=r'\(\sigma\)')
a_1 = widgets.BoundedFloatText(
    value=0.7,
    min=0,
    max=1,
    step=0.05,
    description=r'\(a_1\)')
a_2 = widgets.BoundedFloatText(
    value=0.3,
    min=0,
    max=1,
    step=0.05,
    description=r'\(a_2\)')
A = widgets.BoundedFloatText(
    value=1,
    min=0,
    max=100,
    step=0.1,
    description=r'\(A\)')
##########################################################################
display(widgets.HBox([sigma, a_1, a_2, A]), widgets.interactive_output(
    update_plot, {'sigma': sigma, 'a_x': a_1, 'a_y': a_2, 'A': A}))
