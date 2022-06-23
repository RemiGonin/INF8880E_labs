import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

import json

import preprocess
import line_chart
import bar_chart
from modes import MODES, MODE_TO_COLUMN

import helper
import map

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = 'PROJECT | INF8808'

# Line chart
line_data = preprocess.preprocess_line_graph()
fig_line = go.Figure()
fig_line = line_chart.add_line_trace(fig_line, line_data)


# MAP

fig_map = go.Figure()
dfs_map, map_df = preprocess.preprocess_map()

with open("./assets/uk_regions.geojson", encoding="utf-8") as data_file:
    regions_data = json.load(data_file)

locations = preprocess.get_regions(regions_data)
z = len(regions_data['features']) * [1]

fig_map = map.add_choro_trace(
    fig_map, regions_data, map_df, dfs_map, z, locations)

fig_map = helper.adjust_map_style(fig_map)
fig_map = helper.adjust_map_sizing(fig_map)
fig_map = helper.adjust_map_info(fig_map)

# Bar chart
bar_data_abs, bar_data_perc = preprocess.preprocess_bar_chart()
'''
@app.callback(
    [Output('v3-1', 'figure')],
    [Input('radio-items', 'value')],
    [State('bar-graph', 'figure')]
)
'''


@app.callback(
    [Output('v3-1', 'figure'), Output('mode', 'children'),
     Input('radio-items', 'value'),
     State('v3-1', 'figure')]
)
def radio_updated(value, figure):
    '''
        Updates the application after the radio input is modified.
        Args:
            mode: The mode selected in the radio input.
            figure: The figure as it is currently displayed
        Returns:
            new_fig: The figure to display after the change of radio input
            mode: The new mode
    '''
    figure = bar_chart.init_figure()
    new_fig = bar_chart.draw(figure, bar_data_abs,
                             bar_data_perc, MODE_TO_COLUMN[value])
    new_fig = bar_chart.update_y_axis(new_fig, MODE_TO_COLUMN[value])
    return new_fig, value


value = "Valeur"
fig_bar = bar_chart.init_figure()
fig_bar, value = radio_updated(value, fig_bar)

sidebar = html.Div(
    className='sidebar',
    children=[
        dbc.Nav(
            [
                dbc.NavLink("Accueil", href="#home", className="menu"),
                html.Hr(className="mhr"),
                dbc.NavLink("Analyse temporelle",
                            href="#viz1", className="menu"),
                html.Hr(className="mhr"),
                dbc.NavLink("Analyse géographique",
                            href="#viz2", className="menu"),
                html.Hr(className="mhr"),
                dbc.NavLink("Analyse économique",
                            href="#viz3", className="menu"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
)

app.layout = html.Div([sidebar, html.Div(className='content', children=[
    html.Header(children=[
        html.H2('Habitudes alimentaires du Royaume-Uni',
                className="display-4", id="home"),
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
            html.H1('Visualisation 1: Analyse temporelle',
                    className="viz-title", id="viz1"),
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
                    showTips=False,
                    showAxisDragHandles=False,
                    displayModeBar=False),
                className='graph',
                id='v1-1'
            )
        ]),
        html.Div(className='viz-info', children=[
            html.H1('Visualisation 2: Analyse geographique',
                    className="viz-title", id="viz2"),
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
                className='line-graph',
                id='v1-1'
            )
        ]),
        html.Div(className='viz-info', children=[
            html.H1('Visualisation 2: Analyse géographique',
                    className="viz-title", id="viz2"),
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
                className='map-graph',
                id='v2'
            )
        ]),
        html.Div(className='viz-info', children=[
            html.H1('Visualisation 3: Analyse économique',
                    className="viz-title", id="viz3"),
            html.Div(
                '''
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
                        
                    '''
            )
        ]),
        html.Div(className='viz-container', children=[
            dcc.Graph(
                figure=fig_bar,
                config=dict(
                    scrollZoom=False,
                    showTips=False,
                    showAxisDragHandles=False,
                    doubleClick=False,
                    displayModeBar=False
                ),
                className='bar-graph',
                id='v3-1'
            ),
            html.Footer(children=[
                html.Div(className='panel', children=[
                        html.Div(id='info', children=[
                            html.P(
                                'Vous pouvez modifier le mode de visualisation en utilisant les boutons ci-dessous.'),
                            html.P(children=[
                                html.Span(
                                    'Le mode de visualisation est actuellement en '),
                                html.Span(MODES['Valeur'], id='mode')
                            ])
                        ]),
                        html.Div(children=[
                            dcc.RadioItems(
                                id='radio-items',
                                options=[
                                    dict(
                                        label=MODES['Valeur'],
                                        value=MODES['Valeur']),
                                    dict(
                                        label=MODES['Pourcentage'],
                                        value=MODES['Pourcentage']),
                                ],
                                value=MODES['Valeur']
                            )
                        ])
                        ])
            ])
        ]),
    ]),
])])
