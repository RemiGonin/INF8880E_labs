

import plotly.graph_objects as go
import hover_template
# from hover_template import get_hover_template_map


def add_choro_trace(fig_map, regions_data, map_df, dfs_map, category):
    '''
        Adds the choropleth trace, representing UK's regions.



        Args:
            fig_map: The figure to add the choropleth trace to
            regions_data: The data used for the trace
            dfs_map: The dataframe to use for data
        Returns:
            fig: The updated figure with the choropleth trace

    '''

    if category == "Alcoholic drinks" or category == "Soft drinks":
        unit = "ml"
    else:
        unit = "g"

    figure = go.Choroplethmapbox(
        geojson=regions_data,
        locations=map_df.index,
        z=map_df[category],  # only one column is passed in this function
        featureidkey="properties.rgn19nm",
        # hovertemplate=get_hover_template_map(category, unit),
        colorscale="RdBu",
        reversescale=True,
        marker_line_color="white",
        zmid=dfs_map["moy2019"].loc[category][0],
        zmax=map_df[category].max(),
        zmin=map_df[category].min(),
        text=(map_df[category]-dfs_map["moy2019"].loc[category][0]).astype(int),
        colorbar=dict(title=unit+"/pers/week",
                      titleside="top",
                      tickmode="array",
                      tickvals=[map_df[category].min(
                      ), dfs_map["moy2019"].loc[category][0], map_df[category].max()],
                      ticktext=[str(map_df[category].min()), str(
                          dfs_map["moy2019"].loc[category][0]) + " National average", str(map_df[category].max())],
                      ticks="outside"
                      )
    )

    fig_map.add_trace(figure)
    fig_map.update_traces(
        hoverlabel={'namelength': 0},
        hovertemplate=hover_template.get_hover_template_map(unit,dfs_map["moy2019"].loc[category][0]))
    fig_map.data[0].colorbar.x = -0.1

    return fig_map
