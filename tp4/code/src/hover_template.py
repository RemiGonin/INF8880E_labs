'''
    Provides the template for the tooltips.
'''


def get_bubble_hover_template():
    '''
        Sets the template for the hover tooltips.

        Contains four labels, followed by their corresponding
        value and units where appropriate, separated by a
        colon : country, population, GDP and CO2 emissions.

        The labels' font is bold and the values are normal weight

        returns:
            The content of the tooltip
    '''
    # TODO : Generate tooltip
    country = "       <b>Country : </b>%{customdata[0]}<br>"
    population = "       <b>Population : </b>%{marker.size}<br>"
    gdp = "       <b>GDP : </b>%{x:.2f} $ (USD)<br>"
    co2 = "       <b>CO2 emissions : </b>%{y:.2f} metric tonnes"
    return country + population + gdp + co2 + "<extra></extra>"
