'''
    Contains some functions related to the creation of the bar chart.
    The bar chart displays the data either as counts or as percentages.
'''

import plotly.graph_objects as go
import plotly.io as pio

import plotly.express as px

from hover_template import get_hover_template_barchart
from modes import MODES, MODE_TO_COLUMN

import pandas as pd


def init_figure():
    """
    Initializes the figure to draw the bar chart on.

    Returns:
        plotly.graph_objects.Figure: The figure to draw on.
    """
    fig = go.Figure()

    fig.update_layout(
        title="Variation des dépenses alimentaires selon les revenus pour l'année 2019",
        template=pio.templates['simple_white'],
        dragmode=False,
        barmode='relative',
        yaxis={'title': 'Dépenses (en pences par personne par semaine)'},
        xaxis={'title': 'Tranches de revenus annuels'}
    )

    return fig


def draw(fig, data_abs, data_perc, mode):
    """
    Draws the bar chart.

    Args:
        fig (plotly.graph_objects.Figure): The figure to draw on.
        data_abs (pandas.DataFrame): The data to display as absolute values.
        data_perc (pandas.DataFrame): The data to display as percentages.
        mode (str): The mode to display the data in.
    Returns:
        plotly.graph_objects.Figure: The figure with the bar chart drawn.
    """

    fig = go.Figure(fig)

    df_data = {"Catégorie": data_abs.index.tolist(),
               "Valeur": data_abs.values.tolist(),
               "Pourcentage": data_perc.values.tolist()}
    df = pd.DataFrame(df_data)

    for category in set(df["Catégorie"]):
        fig.add_trace(go.Bar(x=list(range(1, 11)), y=list(df.loc[df['Catégorie'] == category][mode])[
                      0], name=category, hovertemplate=get_hover_template_barchart(category, mode), hoverlabel={'namelength': 0}))

    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            ticktext=['< 14k £', '15k £ à 18k £', '19k £ à 22k £', '23k £ à 26k £', '27k £ à 30k £',
                      '31k £ à 35k £', '36k £ à 40k £', '41k £ à 49k £', '50k £ à 62k £', '> 62k £']
        )
    )
    return fig


def update_y_axis(fig, mode):
    """
    Updates the y axis of the figure.

    Args:
        fig (plotly.graph_objects.Figure): The figure to update.
        mode (str): The mode to display the data in.
    Returns:
        plotly.graph_objects.Figure: The figure with the y axis updated.
    """
    if mode == "Valeur":
        fig.update_layout(
            yaxis={'title': 'Dépenses (en livres par personne par semaine)'}
        )
    else:
        fig.update_layout(
            yaxis={
                'title': 'Dépenses (en pourcentage par personne par semaine)'}
        )

    return fig
