

import plotly.graph_objects as go


def add_choro_trace(fig_map, regions_data, map_df, dfs_map, z_vals, locations):
    '''
        Adds the choropleth trace, representing UK's regions.



        Args:
            fig_map: The figure to add the choropleth trace to
            regions_data: The data used for the trace
            dfs_map: The dataframe to use for data
        Returns:
            fig: The updated figure with the choropleth trace

    '''

    print(dfs_map["moy2019"])
    figure = go.Choroplethmapbox(
        geojson=regions_data,
        locations=map_df.index,
        z=map_df["Alcoholic drinks"],
        featureidkey="properties.rgn19nm",
        # hovertemplate=hover.map_base_hover_template(),
        colorscale="RdBu",
        reversescale=True,
        marker_line_color="white",
        zmid=dfs_map["moy2019"].loc["Alcoholic drinks"][0],
        # colorbar=dict(thicknessmode='pixels',
        #               thickness=0,
        #               borderwidth=0,
        #               outlinewidth=0,
        #               showticklabels=False,
        #               ypad=0,
        #               xpad=0,
        #               tickwidth=0,
        #               ticklen=0,
        #               len=0
        #               )
    )

    fig_map.add_trace(figure)
    return fig_map
