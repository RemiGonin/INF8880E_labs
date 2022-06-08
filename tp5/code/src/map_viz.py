'''
    Contains the functions to set up the map visualization.

'''

import plotly.graph_objects as go
import plotly.express as px

import hover_template as hover


def add_choro_trace(fig, montreal_data, locations, z_vals, colorscale):
    '''
        Adds the choropleth trace, representing Montreal's neighborhoods.

        Note: The z values and colorscale provided ensure every neighborhood
        will be grey in color. Although the trace is defined using Plotly's
        choropleth features, we are simply defining our base map.

        Args:
            fig: The figure to add the choropleth trace to
            montreal_data: The data used for the trace
            locations: The locations (neighborhoods) to show on the trace
            z_vals: The table to use for the choropleth's z values
            colorscale: The table to use for the choropleth's color scale
        Returns:
            fig: The updated figure with the choropleth trace

    '''

    figure = go.Choroplethmapbox(
        geojson=montreal_data,
        locations=locations,
        z=z_vals,
        featureidkey="properties.NOM",
        hovertemplate=hover.map_base_hover_template(),
        colorscale=colorscale,
        marker_line_color="white",
        colorbar = dict(thicknessmode='pixels',
        thickness=0,
        borderwidth=0,
        outlinewidth=0,
        showticklabels=False,
        bgcolor='white',
        ypad=0,
        xpad=0
        )
    )

    fig.add_trace(figure)
    return fig


def add_scatter_traces(fig, street_df):
    '''
        Adds the scatter trace, representing Montreal's pedestrian paths.

        Args:
            fig: The figure to add the scatter trace to
            street_df: The dataframe containing the information on the
                pedestrian paths to display
        Returns:
            The figure now containing the scatter trace

    '''
    # TODO : Add the scatter markers to the map base
    figure = go.Scattermapbox(
        lat=street_df["properties.LATITUDE"],
        lon=street_df["properties.LONGITUDE"],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=17,
            opacity=0.7
        ),
        text=street_df["properties.NOM_PROJET"],
    )
    return fig.add_trace(figure)
