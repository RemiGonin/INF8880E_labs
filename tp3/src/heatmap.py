'''
    Contains some functions related to the creation of the heatmap.
'''
import plotly.express as px
import hover_template


def get_figure(data):
    '''
        Generates the heatmap from the given dataset.

        Make sure to set the title of the color bar to 'Trees'
        and to display each year as an x-tick.

        Args:
            data: The data to display
        Returns:
            The figure to be displayed.
    '''

    # TODO : Create the heatmap. Make sure to set dragmode=False in
    # the layout. Also don't forget to include the hover template.

    fig = px.imshow(
        data,
        labels={'x': 'Year', 'y': 'District', 'color': 'Trees'})

    fig.update_xaxes(dtick=1)
    fig.update_traces(hoverlabel={'namelength': 0},
                      hovertemplate=hover_template.get_heatmap_hover_template())
    fig.update_layout(dragmode=False)

    return fig
