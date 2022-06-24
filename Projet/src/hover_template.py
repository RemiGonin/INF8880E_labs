'''
    Provides the template for the hover tooltips.
'''


def get_hover_template_barchart(category, mode):
    '''
        Sets the template for the hover tooltips.

        Args:
            name: The hovered element's category
            mode: The current display mode
        Returns:
            The hover template with the elements descibed above
    '''

    if mode == 'Valeur':
        hoverTemplate = '<b>' + category + ' : </b>' + '%{y:.2f} £'
    elif mode == 'Pourcentage':
        hoverTemplate = '<b>' + category + ' : </b>' + '%{y:.2f} %'
    return hoverTemplate


def get_hover_template_linechart():
    '''
        Sets the template for the hover tooltips in the line chart

        The labels are font 'Roboto Slab' and bold. The values
        are font 'Roboto' and regular weight.
    '''

    year = "<span style='font-family: Roboto'><b style='font-family: Roboto Slab'>Année : </b>%{x}</span><br>"
    pence = '<span style="font-family: Roboto"><b style="font-family: Roboto Slab">Dépenses : </b>%{y} £</span><br>'

    return year+pence


def get_hover_template_map(unit, reference):
    '''
        Sets the template for the hover tooltips in the map

        The labels are font 'Roboto Slab' and bold. The values
        are font 'Roboto' and regular weight.
    '''

    region = "<span style='font-family: Roboto'><b style='font-family: Roboto Slab'>Région : </b>%{properties.rgn19nm}</span><br>"
    if unit == "ml":
        val = '<span style="font-family: Roboto"><b style="font-family: Roboto Slab">Quantité : </b>%{z}ml</span><br>'
        offset = '<span style="font-family: Roboto"><b style="font-family: Roboto Slab">Êcart : </b>%{text}ml</span><br>'
    else:
        val = '<span style="font-family: Roboto"><b style="font-family: Roboto Slab">Quantité : </b>%{z}g</span><br>'
        offset = '<span style="font-family: Roboto"><b style="font-family: Roboto Slab">Êcart : </b>%{text}g</span><br>'

    return region+val+offset
