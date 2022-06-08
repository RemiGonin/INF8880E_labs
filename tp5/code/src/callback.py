'''
    This file contains the functions to call when
    a click is detected on the map, depending on the context
'''
import dash_html_components as html


def no_clicks(style):
    '''
        Deals with the case where the map was not clicked

        Args:
            style: The current display style for the panel
        Returns:
            title: The updated display title
            mode: The updated display title
            theme: The updated display theme
            style: The updated display style for the panel
    '''

    return None, None, None, style


def map_base_clicked(title, mode, theme, style):
    '''
        Deals with the case where the map base is
        clicked (but not a marker)

        Args:
            title: The current display title
            mode: The current display title
            theme: The current display theme
            style: The current display style for the panel
        Returns:
            title: The updated display title
            mode: The updated display title
            theme: The updated display theme
            style: The updated display style for the panel
    '''

    return title, mode, theme, style


def map_marker_clicked(figure, curve, point, title, mode, theme, style):  # noqa : E501 pylint: disable=unused-argument too-many-arguments line-too-long
    '''
        Deals with the case where a marker is clicked

        Args:
            figure: The current figure
            curve: The index of the curve containing the clicked marker
            point: The index of the clicked marker
            title: The current display title
            mode: The current display title
            theme: The current display theme
            style: The current display style for the panel
        Returns:
            title: The updated display title
            mode: The updated display title
            theme: The updated display theme
            style: The updated display style for the panel
    '''

    style = {
        'border': '1px solid black',
        'padding': '10px'}

    nom_projet = figure["data"][curve]["customdata"][0][point]
    mode_implantation = figure["data"][curve]["customdata"][1][point]
    objectif_thematique = figure["data"][curve]["customdata"][2][point]

    if objectif_thematique:
        theme = html.Div([html.P('Thématique :'),
                          html.Ul([html.Li(x) for x in objectif_thematique.split('\n')])])
    else:
        theme = ""

    nom_projet = html.Div(style={
                          'color': figure["layout"]['template']['layout']['colorway'][curve]}, children=nom_projet)

    return nom_projet, mode_implantation, theme, style
