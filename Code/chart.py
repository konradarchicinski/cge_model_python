import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json

def create_plot(data_res):

    trace1 = go.Scatter(
        x = data_res.columns,
        y = data_res.loc['HOU_0-30_Wealth'],
        name='HOU_0-30_Wealth',
        line = dict(color='rgb(0,100,80)', width=4)
    )
    trace2 = go.Scatter(
        x = data_res.columns,
        y = data_res.loc['HOU_30-60_Wealth'],
        name='HOU_30-60_Wealth',
        line = dict(color='rgb(67,67,67)', width=4)
    )
    trace3 = go.Scatter(
        x = data_res.columns,
        y = data_res.loc['HOU_60-90_Wealth'],
        name='HOU_60-90_Wealth',
        line = dict(color='rgb(115,115,115)', width=4)
    )
    trace4 = go.Scatter(
        x = data_res.columns,
        y = data_res.loc['HOU_90-95_Wealth'],
        name='HOU_90-95_Wealth',
        line = dict(color='rgb(49,130,189)', width=4)
    )
    trace5 = go.Scatter(
        x = data_res.columns,
        y = data_res.loc['HOU_95-100_Wealth'],
        name='HOU_95-100_Wealth',
        line = dict(color='rgb(189,189,189)', width=4)
    )

    layout = go.Layout(
        autosize=False,
        width=1100,
        height=600,
        plot_bgcolor='#FFFFFF'
    )

    data = [trace1, trace2, trace3, trace4, trace5]
    fig = go.Figure(data=data, layout=layout)
    fig.update_xaxes(nticks=len(data_res.columns))

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON