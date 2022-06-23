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
import mapBarChart

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = 'PROJECT | INF8808'

# Line chart
line_data = preprocess.preprocess_line_graph()
fig_line = go.Figure()
fig_line = line_chart.add_line_trace(fig_line, line_data)

# Bar chart
bar_data_abs, bar_data_perc = preprocess.preprocess_bar_chart()


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

# MAP

dfs_map, map_df = preprocess.preprocess_map()

with open("./assets/uk_regions.geojson", encoding="utf-8") as data_file:
    regions_data = json.load(data_file)


categories = list(map_df.columns)
categories = [" " + cat + "    " for cat in categories]


@app.callback(
    Output("v2", "figure"),
    Input("category", "value"))
def display_choropleth(category):
    category = category[1:-4]  # remove spaces
    fig_map = go.Figure()
    fig_map = map.add_choro_trace(
        fig_map, regions_data, map_df, dfs_map, category)
    fig_map.update_geos(fitbounds="locations", visible=False)
    fig_map.update_layout(margin={"r": 0, "t": 0, "l": 10, "b": 0})

    fig_map = helper.adjust_map_style(fig_map)
    fig_map = helper.adjust_map_sizing(fig_map)
    fig_map = helper.adjust_map_info(fig_map)

    return fig_map


@app.callback(
    Output('v2bar', 'figure'),
    [Input('v2', 'clickData'),
     Input("category", "value")]
)
def map_clicked(click_data, category):
    category = category[1:-4]  # remove spaces

    # handle when nothing is clicked:
    if click_data is None or click_data['points'][0]['z'] == 0:
        fig = mapBarChart.get_empty_figure()
        mapBarChart.add_rectangle_shape(fig)
        return fig

    fig = mapBarChart.get_figure(click_data, dfs_map, category)
    return fig


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
                La nutrition est un facteur clé dans toute population. Elle permet de mesurer la santé d’une population, 
                ses habitudes, ou de tirer des conclusions sur ses habitudes économiques et sociales. La nutrition et les 
                habitudes alimentaires de manière plus générale évoluent constamment, au fur et à mesure que les sociétés se développent.
            ''', style={'text-align': 'justify'}),
        html.Div(
            '''     
                L’importance cruciale de ces données a poussé de nombreux gouvernements à recenser la consommation alimentaire de 
                leur population, et de les analyser. C’est notamment le cas du gouvernement des Royaumes Unis qui ont réalisé plusieurs 
                statistiques sur l’alimentation de leur population. Ils ont, pour illustrer, analysé combien une personne dépense en moyenne
                en nourriture et en livraison de plats par semaine. Le but étant de comprendre l'évolution des habitudes alimentaires des habitants.
        ''', style={'text-align': 'justify'}),
        html.Div(
            '''        
                L’objectif ici sera de déterminer les habitudes alimentaires des habitants du Royaume-Uni en fonction de divers facteurs 
                (région, revenu, statut économique, …) et aussi de voir les évolutions de ces habitudes au fil du temps, de 1974 à 2020. 
                Ces habitudes alimentaires peuvent être analysées grâce aux dépenses des foyers ainsi que les quantités de nourritures achetées.
        ''', style={'text-align': 'justify'}),
        html.Div(
            '''        
                Les données proviennent du site officiel du gouvernement britannique : https://www.gov.uk/government/statistical-data-sets/family-food-datasets.
                
            ''', style={'text-align': 'justify'})
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
            html.H1('Visualisation 2: Analyse géographique',
                    className="viz-title", id="viz2"),
            html.Div(
                '''
                        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
                    '''
            )
        ]),

        html.Div(className='viz-container',
                 style={'width': '100%', 'display': 'inline-block'},
                 children=[
                     html.H4(
                         "Habitudes alimentaires des foyers anglais par région, par catégorie", style={"margin-left": "5%"}),
                     html.P("Selectionner une catégorie:", style={
                            "font-weight": "bold", "margin-left": "10%", "margin-right": "10%"}),
                     html.Div(
                         dcc.RadioItems(
                             id="category",
                             options=categories,
                             value=" Alcoholic drinks    ",

                         ), style={'display': 'block', "margin-left": "10%", "margin-right": "10%"},
                     ),
                     # MAP
                     html.Div(
                         dcc.Graph(
                             config=dict(
                                 scrollZoom=False,
                                 showTips=False,
                                 showAxisDragHandles=False,
                                 doubleClick=False,
                                 displayModeBar=False
                             ),
                             className='graph',
                             id='v2',

                         ), style={'display': 'inline-block'}),
                     # MAP-BARCHART
                     html.Div(
                         dcc.Graph(
                             config=dict(
                                 scrollZoom=False,
                                 showTips=False,
                                 showAxisDragHandles=False,
                                 doubleClick=False,
                                 displayModeBar=False
                             ),
                             className='graph',
                             id='v2bar',
                         ), style={'display': 'inline-block'})
                 ]),
        html.Div(className='viz-info', children=[
            html.H1('Visualisation 3: Analyse économique',
                    className="viz-title", id="viz3"),
            html.Div(
                '''
                    Dans cette partie, nous avons voulu répondre à la question : comment varient 
                    les dépenses dans les différentes catégories d’aliments (viandes, fruits et légumes, alcool, …) 
                    des foyers anglais selon leur revenu ?
                ''', style={'text-align': 'justify'}),
            html.Div(
                '''
                    Nous avons voulu explorer les évolutions données de consommation en fonction des tranches de revenu des personnes.
                    Les données sont donc découpées par décile (les données de déciles viennent du site : https://www.gov.uk/government/statistics/percentile-points-from-1-to-99-for-total-income-before-and-after-tax).
                    Les données sont présentées ici sous une forme brute (valeur absolue des dépenses de consommations par catégorie) 
                    mais aussi en pourcentage. L'idée de la première visualisation est d'observer les différences de dépenses brutes dans la consommation (par exemple, les plus aisés dépensent plus que les moins aisés), 
                    alors que la deuxième visualisation en pourcentage permet d'observer les différences dans la consommation (par exemple, une tranche de revenu consomme en proportion plus d'un type d'aliment qu'une autre tranche).
                    Il est possible de passer d'une visualisation à l'autre en cliquant sur les boutons en dessous.
                ''', style={'text-align': 'justify'}),
            html.Div(
                '''
                    Au niveau des résultats, on observe pour la visualisation en valeur que les tranches à haut revenus dépenses en moyenne plus que les autres tranches. 
                    Ceci paraît plutôt logique et peut s'expliquer par différentes choses : un plus gros budget alloué à l'alimentation (permis par un plus gros budget en général), des dépenses dans des produits de qualités supérieures, 
                    plus de dépenses "excessives".
                ''', style={'text-align': 'justify'}),
            html.Div(
                '''
                    Au niveau de la deuxième visualisation en pourcentage, on peut observer que les classes les moins aisées consomment moins de fruits et légumes et plus de produits à base de céréales.
                    Inversement, les tranches les plus aisées consomment plus de légumes que les autres tranches. Elles dépensent aussi plus dans l'alcool que les autres.
                ''', style={'text-align': 'justify'})
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
            html.P(
                'Vous pouvez modifier le mode de visualisation en utilisant les boutons ci-dessous.'),
            html.P(children=[
                html.Span('Le mode de visualisation est actuellement en '),
                html.Span(MODES['Valeur'], id='mode')]),
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

        ], style={"margin-left": "50px"})])])])
