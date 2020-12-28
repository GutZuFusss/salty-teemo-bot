import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque


num_bets = deque()
num_bets.append(0)
red_bets = deque()
red_bets.append(0)
blue_bets = deque()
blue_bets.append(0)


initial_trace = plotly.graph_objs.Scatter(
    x=list(red_bets),
    y=list(num_bets),
    name='Scatter',
    mode='lines+markers'
)

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph',
                  animate=True,
                  figure={'data': [initial_trace],
                          'layout': go.Layout(
                                xaxis=dict(range=[min(num_bets), max(num_bets)]),
                                yaxis=dict(range=[min(red_bets + blue_bets), max(red_bets + blue_bets)]),
                                plot_bgcolor='rgb(10,10,10)'
                                )
                          }),
        dcc.Interval(
            id='graph-update',
            interval=1*1000
        ),
    ]
)


def update_bets(bets):
    num_bets.append(num_bets[-1] + 1)
    red_bets.append(bets[0])
    blue_bets.append(bets[1])

def reset_bets():
    num_bets.clear()
    num_bets.append(0)
    red_bets.clear()
    red_bets.append(0)
    blue_bets.clear()
    blue_bets.append(0)



@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph_scatter(n):
    sc_red_bets = go.Scatter(
        x=list(num_bets),
        y=list(red_bets),
        name='BetsRed',
        mode='lines+markers',
        marker=dict(
            color='#e65555',
            size=12,
            line=dict(
                color='#830000',
                width=2
            )
        )
    )

    sc_blue_bets = go.Scatter(
        x=list(num_bets),
        y=list(blue_bets),
        name='BetsBlue',
        mode='lines+markers',
        marker=dict(
            color='#339fff',
            size=12,
            line=dict(
                color='#3333ff',
                width=2
            )
        )
    )

    return {'data': [sc_red_bets, sc_blue_bets],
            'layout': go.Layout(
                xaxis=dict(range=[min(num_bets), max(num_bets) + 1]),
                yaxis=dict(range=[min(red_bets + blue_bets), max(red_bets + blue_bets) + 200]),
                plot_bgcolor='rgb(10,10,10)'
                )
            }


def start_web_gui():
    app.run_server(debug=True)
