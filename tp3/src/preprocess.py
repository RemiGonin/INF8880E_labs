'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd


def convert_dates(dataframe):
    '''
        Converts the dates in the dataframe to datetime objects.

        Args:
            dataframe: The dataframe to process
        Returns:
            The processed dataframe with datetime-formatted dates.
    '''
    dataframe["Date_Plantation"] = pd.to_datetime(dataframe["Date_Plantation"])
    return dataframe


def filter_years(dataframe, start, end):
    '''
        Filters the elements of the dataframe by date, making sure
        they fall in the desired range.

        Args:
            dataframe: The dataframe to process
            start: The starting year (inclusive)
            end: The ending year (inclusive)
        Returns:
            The dataframe filtered by date.
    '''

    dataframe = dataframe[dataframe["Date_Plantation"].dt.year >= start]
    dataframe = dataframe[dataframe["Date_Plantation"].dt.year <= end]
    dataframe = dataframe.reset_index(drop=True)

    return dataframe


def summarize_yearly_counts(dataframe):
    '''
        Groups the data by neighborhood and year,
        summing the number of trees planted in each neighborhood
        each year.

        Args:
            dataframe: The dataframe to process
        Returns:
            The processed dataframe with column 'Counts'
            containing the counts of planted
            trees for each neighborhood each year.
    '''
    serie = dataframe.groupby(["Arrond_Nom", dataframe.Date_Plantation.dt.year]
                              ).size()
    df = serie.rename("Counts").to_frame()

    return df


def restructure_df(yearly_df):
    '''
        Restructures the dataframe into a format easier
        to be displayed as a heatmap.

        The resulting dataframe should have as index
        the names of the neighborhoods, while the columns
        should be each considered year. The values
        in each cell represent the number of trees
        planted by the given neighborhood the given year.

        Any empty cells are filled with zeros.

        Args:
            yearly_df: The dataframe to process
        Returns:
            The restructured dataframe
    '''

    # To pivot the dataframe we need to set index as Arrond_Nom
    yearly_df = yearly_df.reset_index().set_index("Arrond_Nom")

    # Pivot to get the dataframe with the right format
    yearly_df = yearly_df.pivot_table(values="Counts",
                                      index=yearly_df.index, columns="Date_Plantation", aggfunc='first')
    # Fill NaN with 0:
    yearly_df = yearly_df.fillna(0)

    return yearly_df


def get_daily_info(dataframe, arrond, year):
    '''
        From the given dataframe, gets
        the daily amount of planted trees
        in the given neighborhood and year.

        Args:
            dataframe: The dataframe to process
            arrond: The desired neighborhood
            year: The desired year
        Returns:
            The daily tree count data for that
            neighborhood and year.
    '''

    # Filter dataframe by arond #
    dataframe = dataframe[dataframe["Arrond"] == arrond]

    # Filter dataframe by arond name
    #dataframe = dataframe[dataframe["Arrond_Nom"] == arrond]

    # Filter dataframe by year
    dataframe = dataframe[dataframe["Date_Plantation"].dt.year == year]

    # get daily values
    daily_values = dataframe.groupby(["Date_Plantation"]).size()

    return daily_values
