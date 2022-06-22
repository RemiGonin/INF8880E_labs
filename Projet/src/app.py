import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

import preprocess
import line_chart

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = 'PROJECT | INF8808'

line_data = preprocess.preprocess_line_graph()

fig_line = go.Figure()
fig_line = line_chart.add_line_trace(fig_line, line_data)

sidebar = html.Div(
    className='sidebar',
    children=[
        dbc.Nav(
            [
                dbc.NavLink("Acceuil", href="#home", className="menu"),
                html.Hr(className="mhr"),
                dbc.NavLink("Analyse temporelle", href="#viz1", className="menu"),
                html.Hr(className="mhr"),
                dbc.NavLink("Analyse geographique", href="#viz2", className="menu"),
                html.Hr(className="mhr"),
                dbc.NavLink("Analyse economique", href="#viz3", className="menu"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
)

app.layout = html.Div([sidebar, html.Div(className='content', children=[
        html.Header(children=[
            html.H2('Habitudes alimentaires du Royaume-Uni', className="display-4", id="home"),
        ]),
        html.Hr(className="headhr"),
        html.Div(className="viz-info", children=[
            html.Div(
                        '''
                            Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
                        '''
                    )
        ]),
        html.Main(children=[
            html.Div(className='viz-info', children=[
                html.H1('Visualisation 1: Analyse temporelle', className="viz-title", id="viz1"),
                html.Div(
                    '''
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
                    '''
                )
            ]), 
            html.Div(className='viz-container', children=[
                dcc.Graph(
                    figure=fig_line,
                    config=dict(
                        scrollZoom=False,
                        showTips=False,
                        showAxisDragHandles=False,
                        doubleClick=False,
                        displayModeBar=False
                    ),
                    className='graph',
                    id='v1-1'
                )
            ]),
            html.Div(className='viz-info', children=[
                html.H1('Visualisation 2: Analyse geographique', className="viz-title", id="viz2"),
                html.Div(
                    '''
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
                    '''
                )
            ]),
            html.Div(className='viz-container', children=[
                dcc.Graph(
                    figure=go.Figure(),
                    config=dict(
                        scrollZoom=False,
                        showTips=False,
                        showAxisDragHandles=False,
                        doubleClick=False,
                        displayModeBar=False
                    ),
                    className='graph',
                    id='v2'
                )
            ]),
            html.Div(className='viz-info', children=[
                html.H1('Visualisation 3: Analyse economique', className="viz-title", id="viz3"),
                html.Div(
                    '''
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
                        
                    '''
                )
            ]),
            html.Div(className='viz-container', children=[
                dcc.Graph(
                    figure=go.Figure(),
                    config=dict(
                        scrollZoom=False,
                        showTips=False,
                        showAxisDragHandles=False,
                        doubleClick=False,
                        displayModeBar=False
                    ),
                    className='graph',
                    id='v3-1'
                )
            ]),
            
        ]),
    ])])
