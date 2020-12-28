import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque


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
                                        yaxis=dict(range=[min(self.red_bets + self.blue_bets), max(self.red_bets + self.blue_bets)]),
                                        plot_bgcolor='rgb(10,10,10)'
                                        )
                                }),
                dcc.Interval(
                    id='graph-update',
                    interval=1*1000
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

    def update_graph_scatter(self, n): # TODO: self? xd
        sc_red_bets = go.Scatter(
            x=list(self.num_bets),
            y=list(self.red_bets),
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
            x=list(self.num_bets),
            y=list(self.blue_bets),
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
                    xaxis=dict(range=[min(self.num_bets), max(self.num_bets) + 1]),
                    yaxis=dict(range=[min(self.red_bets + self.blue_bets), max(self.red_bets + self.blue_bets) + 200]),
                    plot_bgcolor='rgb(10,10,10)'
                    )
                }

    def start(self):
        self.app.run_server(debug=True)