'''
    Contains some functions related to the creation of the line chart.
'''
from numpy import size
import plotly.express as px
import hover_template
import plotly.graph_objects as go


from template import THEME


def get_empty_figure():
    '''
        Returns the figure to display when there is no data to show.

        The text to display is : 'No data to display. Select a cell
        in the heatmap for more information.

    '''

    # TODO : Construct the empty figure to display. Make sure to
    # set dragmode=False in the layout.

    fig = go.Figure(go.Scatter(x=[], y=[]))
    #fig = px.line(None)

    fig.add_annotation(
        text='No data to display. Select a cell in the heatmap for more information.',
        y=0.5,
        font=dict(color="black", size=12),
        showarrow=False)
    fig.update_traces()
    fig.update_xaxes(range=[0, 1], showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(dragmode=False)

    return fig


def add_rectangle_shape(fig):
    '''
        Adds a rectangle to the figure displayed
        behind the informational text. The color
        is the 'pale_color' in the THEME dictionary.

        The rectangle's width takes up the entire
        paper of the figure. The height goes from
        0.25% to 0.75% the height of the figure.
    '''
    # TODO : Draw the rectangle
    fig.add_shape(
        type='rect',
        x0=0,
        y0=0.25,
        x1=1,
        y1=0.75,
        fillcolor=THEME['pale_color'],
    )

    return fig


def get_figure(line_data, arrond, year):
    '''
        Generates the line chart using the given data.

        The ticks must show the zero-padded day and
        abbreviated month. The y-axis title should be 'Trees'
        and the title should indicated the displayed
        neighborhood and year.

        In the case that there is only one data point,
        the trace should be displayed as a single
        point instead of a line.

        Args:
            line_data: The data to display in the
            line chart
            arrond: The selected neighborhood
            year: The selected year
        Returns:
            The figure to be displayed
    '''
    # TODO : Construct the required figure. Don't forget to include the hover template
    if len(line_data) != 1:
        fig = go.Figure(go.Scatter(x=line_data.index,
                        y=line_data.values, mode='lines'))
        fig.update_xaxes(showticklabels=True, tickangle=-
                         45, dtick='M1', tickformat='%d %b')

    elif len(line_data) == 1:
        fig = go.Figure(go.Scatter(x=line_data.index,
                        y=line_data.values, mode='markers'))
        fig.update_xaxes(showticklabels=True, tickangle=-
                         45, tickformat='%d %b')

    fig.update_layout(
        title='Trees planted in ' + str(arrond) + ' in ' + str(year))
    fig.update_yaxes(title='Trees', showticklabels=True)
    fig.update_traces(
        hoverlabel={'namelength': 0},
        hovertemplate=hover_template.get_linechart_hover_template())

    return fig
