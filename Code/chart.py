import plotly as py
import plotly.graph_objs as go
import ipywidgets as widgets
import numpy as np


def utility_function_chart(sigma=0.5, a_x=0.7, a_y=0.3, A=1):
    
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


    def prod_fun(X, Y):
        return A * (((a_x * X)**(1 / sigma))**(sigma - 1) + \
                    ((a_y * Y)**(1 / sigma))**(sigma - 1))**(sigma / (sigma - 1))

    surface = go.Surface(
        x=X1,
        y=X2,
        z=prod_fun(X1,X2),
        colorscale="Blues",
        colorbar={
            "title": "Function value",
            "len": 1.0,
            "thickness": 20
        }
    )
    fig = go.Figure(data=surface, layout=layout)
    fig.update_traces(
        contours_z=dict(
            show=True,
            usecolormap=False,
            project_z=True))

    py.offline.iplot(fig)


if __name__ == "__main__":

    utility_function_chart()