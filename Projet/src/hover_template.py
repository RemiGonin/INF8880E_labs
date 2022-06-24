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

def get_hover_template_linechart():
    '''
        Sets the template for the hover tooltips in the heatmap.

        Contains two labels, followed by their corresponding
        value, separated by a colon : date and trees planted.

        The labels are font 'Roboto Slab' and bold. The values
        are font 'Roboto' and regular weight.
    '''

    year = "<span style='font-family: Roboto'><b style='font-family: Roboto Slab'>Année : </b>%{x}</span><br>"
    pence = '<span style="font-family: Roboto"><b style="font-family: Roboto Slab">Dépenses : </b>%{y} £</span><br>'

    return year+pence

def get_hover_template_map(unit, reference):
    '''
        Sets the template for the hover tooltips in the heatmap.

        Contains two labels, followed by their corresponding
        value, separated by a colon : date and trees planted.

        The labels are font 'Roboto Slab' and bold. The values
        are font 'Roboto' and regular weight.
    '''

    region = "<span style='font-family: Roboto'><b style='font-family: Roboto Slab'>Région : </b>%{properties.rgn19nm}</span><br>"
    if unit=="ml":
        val = '<span style="font-family: Roboto"><b style="font-family: Roboto Slab">Quantité : </b>%{z}ml</span><br>'
        offset = '<span style="font-family: Roboto"><b style="font-family: Roboto Slab">Êcart : </b>%{text}ml</span><br>'
    else:
        val = '<span style="font-family: Roboto"><b style="font-family: Roboto Slab">Quantité : </b>%{z}g</span><br>'
        offset = '<span style="font-family: Roboto"><b style="font-family: Roboto Slab">Êcart : </b>%{text}g</span><br>'
    

    return region+val+offset