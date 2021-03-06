import plotly.graph_objects as go


def get_empty_figure():
    '''
        Returns the figure to display when there is no data to show.
    '''

    fig = go.Figure(go.Bar(x=[], y=[]))

    fig.add_annotation(
        text="Aucune donnée a afficher. Cliquez sur une région de la carte pour plus avoir plus d'information.",
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
        behind the informational text.
    '''
    fig.add_shape(
        type='rect',
        x0=0,
        y0=0.25,
        x1=1,
        y1=0.75,
        fillcolor="#DFD9E2",
    )

    return fig


def get_figure(regionData, dfs_map, category):

    region = regionData["points"][0]["location"]

    average = dfs_map["moy2019"].loc[category][0]

    dfs_map = dfs_map[region].drop(columns=["Units"])
    x = list(dfs_map.columns)

    y = dfs_map.loc[category].tolist()
    y = (y-average)/average.round(1)

    fig = go.Figure()

    fig.add_trace(go.Bar(x=x, y=y,  marker=dict(
        color=y, colorscale="RdBu", reversescale=True, cmid=0)))
    fig.update_yaxes(tickformat=".1%")
    if category == "Alcoholic drinks" or category == "Soft drinks":
        unit = "ml"
    else:
        unit = "g"

    trad_dic = {"Milk, milk products and cheese": "Lait, produits laitiers et fromages", "Meat and fish": "Viandes et poissons", "Fruits and vegetables": "Fruits et légumes",
                "Cetreal products, bread, and flour": "Produits céréaliers, pain et farines", "Cakes, pastries and biscuits": "Gateaux, patisseries et biscuits", "Alcoholic drinks": "Boissons alcoolisées", "Soft drinks": "Boissons sucrées"}
    fig.update_layout(
        title="Différence relative (%) de consommation de " + trad_dic[str(category)].lower(
        ) + " par personne <br>et par semaine  dans la région " + str(region) + "<br>comparé à la moyenne nationale en 2019 : " + str(average) + unit)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)")
    return fig
