import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque


GRAPH_UPDATE_INTERVAL = 1000
GRAPH_H_MULTIPLIER = 1.05
PLOT_BG_COLOR = 'rgb(10,10,10)'
GRAPH_MARKERS_SIZE = 12
RED_MARKERS_INNER = '#e65555'
RED_MARKERS_OUTTER = '#830000'
BLUE_MARKERS_INNER = '#339fff'
BLUE_MARKERS_OUTER = '#3333ff'

class WebApp:
    def __init__(self):
        self.num_bets = deque()
        self.num_bets.append(0)
        self.red_bets = deque()
        self.red_bets.append(0)
        self.blue_bets = deque()
        self.blue_bets.append(0)

        self.initial_trace = plotly.graph_objs.Scatter(
            x=list(self.red_bets),
            y=list(self.num_bets),
            name='Scatter',
            mode='lines+markers'
        )

        self.app = dash.Dash(__name__)
        self.app.layout = html.Div(
            [
                dcc.Graph(id='live-graph',
                        animate=True,
                        figure={'data': [self.initial_trace],
                                'layout': go.Layout(
                                        xaxis=dict(range=[min(self.num_bets), max(self.num_bets)]),
                                        yaxis=dict(range=[0, self.calc_max_graph_height()]),
                                        plot_bgcolor=PLOT_BG_COLOR
                                        )
                                }),
                dcc.Interval(
                    id='graph-update',
                    interval=GRAPH_UPDATE_INTERVAL
                ),
            ]
        )

        self.app.callback(Output('live-graph', 'figure'),
                        [Input('graph-update', 'n_intervals')])(self.update_graph_scatter)


    def update_bets(self, bets):
        self.num_bets.append(self.num_bets[-1] + 1)
        self.red_bets.append(bets[0])
        self.blue_bets.append(bets[1])

    def reset_bets(self):
        self.num_bets.clear()
        self.num_bets.append(0)
        self.red_bets.clear()
        self.red_bets.append(0)
        self.blue_bets.clear()
        self.blue_bets.append(0)

    def update_graph_scatter(self, n):
        sc_red_bets = go.Scatter(
            x=list(self.num_bets),
            y=list(self.red_bets),
            name='Red (total shrooms)',
            mode='lines+markers',
            marker=dict(
                color=RED_MARKERS_INNER,
                size=GRAPH_MARKERS_SIZE,
                line=dict(
                    color=RED_MARKERS_OUTTER,
                    width=2
                )
            )
        )

        sc_blue_bets = go.Scatter(
            x=list(self.num_bets),
            y=list(self.blue_bets),
            name='Blue (total shrooms)',
            mode='lines+markers',
            marker=dict(
                color=BLUE_MARKERS_INNER,
                size=GRAPH_MARKERS_SIZE,
                line=dict(
                    color=BLUE_MARKERS_OUTER,
                    width=2
                )
            )
        )

        return {'data': [sc_red_bets, sc_blue_bets],
                'layout': go.Layout(
                    xaxis=dict(range=[min(self.num_bets), max(self.num_bets) + 1]),
                    yaxis=dict(range=[0, self.calc_max_graph_height()]),
                    plot_bgcolor=PLOT_BG_COLOR
                    )
                }

    def calc_max_graph_height(self):
        h = max(self.red_bets + self.blue_bets)
        h *= GRAPH_H_MULTIPLIER
        return h

    def start(self):
        self.app.run_server(debug=True, use_reloader=False)