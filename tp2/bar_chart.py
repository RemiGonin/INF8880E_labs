'''
    Contains some functions related to the creation of the bar chart.
    The bar chart displays the data either as counts or as percentages.
'''

import plotly.graph_objects as go
import plotly.io as pio

import plotly.express as px

from hover_template import get_hover_template
from template import create_template
from modes import MODES, MODE_TO_COLUMN

import pandas as pd


def init_figure():
    '''
        Initializes the Graph Object figure used to display the bar chart.
        Sets the template to be used to "simple_white" as a base with
        our custom template on top. Sets the title to 'Lines per act'

        Returns:
            fig: The figure which will display the bar chart
    '''
    fig = go.Figure()

    # TODO : Update the template to include our new theme and set the title
    #pio.templates.default = "simple_white+template"
    fig.update_layout(
        title="Lines per act",
        template=pio.templates['simple_white+cust'],
        dragmode=False,
        barmode='relative',
        yaxis={'title':'Line (Count)'}
    )

    return fig


def draw(fig, data, mode):
    '''
        Draws the bar chart.

        Arg:
            fig: The figure comprising the bar chart
            data: The data to be displayed
            mode: Whether to display the count or percent data.
        Returns:
            fig: The figure comprising the drawn bar chart
    '''
    fig = go.Figure(fig)  # conversion back to Graph Object
    # TODO : Update the figure's data according to the selected mode
    df_data = {"Act":data.index.tolist(),
               "Player": data["Player"].values.tolist(),
               "LineCount": data["LineCount"].values.tolist(),
               "LinePercent": data["LinePercent"].values.tolist()}
    df = pd.DataFrame(df_data)
    for p in set(df["Player"]):
        fig.add_trace(go.Bar(x=df.loc[df['Player'] == p]["Act"].tolist(), y=df.loc[df['Player'] == p][mode], name=p))
    fig.update_layout()
    return fig


def update_y_axis(fig, mode):
    '''
        Updates the y axis to say 'Lines (%)' or 'Lines (Count) depending on
        the current display.

        Args:
            mode: Current display mode
        Returns: 
            The updated figure
    '''
    # TODO : Update the y axis title according to the current mode
    if mode == "LineCount":
        fig.update_layout(
            yaxis={'title':'Line (Count)'}
        )
    else:
        fig.update_layout(
            yaxis={'title':'Line (%)'}
        )

    return fig