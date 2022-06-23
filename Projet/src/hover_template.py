'''
    Provides the template for the hover tooltips.
'''


def get_hover_template_barchart(category, mode):
    '''
        Sets the template for the hover tooltips.

        The template contains:
            * A title stating the hovered element's x value, with:
                - Font family: Grenze Gotish
                - Font size: 24px
                - Font color: Black
            * A bold label for the player name followed
                by the hovered elements's player's name
            * A bold label for the player's lines
                followed by:
                - The number of lines if the mode is 'Count'
                - The percent of lines fomatted with two
                    decimal points followed by a '%' symbol
                    if the mode is 'Percent'.

        Args:
            name: The hovered element's player's name
            mode: The current display mode
        Returns:
            The hover template with the elements descibed above
    '''

    if mode == 'Valeur':
        hoverTemplate = '<b>' + category + ' : </b>' + '%{x:.2f} £'
    elif mode == 'Pourcentage':
        hoverTemplate = '<b>' + category + ' : </b>' + '%{x:.2f} %'
    return hoverTemplate


def get_hover_template_map(category, unit):
    '''
    #TODO commentaires
    '''

    hoverTemplate = "<b>" + category + \
        " : </b> %{map_df[category]} " + unit + "<extra></extra>"

    return hoverTemplate
