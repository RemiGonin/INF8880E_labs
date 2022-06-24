import pandas as pd
import numpy as np
import pathlib

#! odfpy needs to be installed : pip install odfpy
try:
    import odf
except ModuleNotFoundError:
    print("odfpy needs to be installed: pip install odfpy")

PATH = pathlib.Path(__file__).parent.parent
DATA_PATH = PATH.joinpath("data").resolve()


def preprocess_sheet(df):
    """


    Removes Major Food Code, Minor Food Code, RSE(a), % change since 201617,
    % change since 201819, sig(b), trend since 201617(c), code and food group columns
    as they are not needed down the line.

    Fixes dates in the header so that they are 1 year

    Groups the data into 7 categories that we want to represent :
    - Milk products + cheese
    - Soft drinks
    - carcase meat / non-carcase meat / fish
    - fruits, vegetables
    - alcoolic beverages
    - Bread + Cereal products + flour
    - Cakes / biscuits 

    Args:
        An excel sheet that has been put in a dataframe, raw

    Returns:
        A dataframe with all the information processed and categorized

    """

    # Get categories possible from merging food category and food group
    cats = pd.concat([df["Food Category"], df["Food Group"]], axis=1)
    cats = cats.fillna('').sum(axis=1).replace("", np.nan)

    df["Category"] = cats
    df = df.set_index("Category")
    df = df.drop(["Food Category", "Food Group"], axis=1)
    df = df[df.index.notnull()]

    # Combine categories and removing redundancy

    # this combines rows, drops the leftover rows and rename the combined row
    df.loc["Milk and milk products excluding cheese"] += df.loc["Cheese"]
    df = df.drop(["Cheese"])
    df = df.rename(index={
                   "Milk and milk products excluding cheese": "Milk, milk products and cheese"})

    df.loc["Cakes, buns and pastries"] += df.loc["Biscuits and crispbreads"]
    df = df.drop(["Biscuits and crispbreads"])
    df = df.rename(index={
                   "Cakes, buns and pastries": "Cakes, pastries and biscuits"})

    df.loc["Carcase meat"] += df.loc["Non-carcase meat and meat products"]
    df.loc["Carcase meat"] += df.loc["Fish"]
    df = df.drop(["Non-carcase meat and meat products"])
    df = df.drop(["Fish"])
    df = df.rename(index={
                   "Carcase meat": "Meat and fish"})

    df.loc["Bread"] += df.loc["White bread"]
    df.loc["Bread"] += df.loc["Brown and wholemeal bread"]
    df.loc["Bread"] += df.loc["Flour"]
    df.loc["Bread"] += df.loc["Other cereals and cereal products"]
    df = df.drop(["White bread"])
    df = df.drop(["Brown and wholemeal bread"])
    df = df.drop(["Flour"])
    df = df.drop(["Other cereals and cereal products"])
    df = df.rename(index={
                   "Bread": "Cereal products, bread, and flour"})

    df = df.rename(index={
                   "Fresh and processed fruit and vegetables, excluding potatoes": "Fruits and vegetables"})

    # droping irrelevant categories or sub-categories
    df = df.drop(["Fresh and processed fruit and vegetables, including potatoes",
                  "Liquid wholemilk, including school and welfare",
                  "Other milk and cream",
                  "Eggs",
                  "Fats",
                  "Sugar and preserves",
                  "Fresh and processed fruit and vegetables, including potatoes",
                  "Fresh and processed vegetables, excluding potatoes",
                  "Fresh and processed potatoes",
                  "Processed potatoes",
                  "Fresh and processed fruit",
                  "Fresh fruit",
                  "Processed fruit and fruit products",
                  "Beverages",
                  "Confectionery",
                  "Fresh and processed vegetables, including potatoes",
                  "Fresh green vegetables",
                  "Other fresh vegetables",
                  "Processed vegetables excluding processed potatoes",
                  "Other food and drink",
                  ])

    # Round the floats to 2 decimal place
    df = df.round(1)

    # fix years
    fixed_years = {}
    for col in df.columns:
        if len(str(col)) == 6:  # YYYYYY format
            fixed_year = int(str(col)[:2] + str(col)[4:])
            fixed_years[col] = fixed_year
        if len(str(col)) == 7:  # YYYY-YY format
            fixed_year = int(str(col)[:4])
            fixed_years[col] = fixed_year

    df = df.rename(columns=fixed_years)

    return df


def preprocess_line_graph():
    """
    Reads and prepares the data for the line graph.

    Returns:
        A dataframe containing quantities of different food categories for 1974 to 2020
    """

    print("line")

    df = pd.read_csv(DATA_PATH.joinpath("expenditure"))

    # Remove columns that we won't use:
    df = df.drop(["Code", "Major Food Code", "Minor Food Code", "RSE indicator(b)", "% change since 201617",
                  "sig(c)", "trend since 201617(d)"], axis=1)

    df = preprocess_sheet(df).drop(["Fresh potatoes"])

    print("line done")
    return df


def preprocess_bar_chart():
    print("barchart")
    """
    Reads and prepares the data for the bar chart.

    Returns:
        A dataframe containing quantities of different food categories for 2019 for every decile
        A dataframe containing percentages quantities of different food categories for 2019 for every decile

    """

    res_df = pd.DataFrame()

    for i in range(1, 11):
        decile = "Decile_" + str(i)
        df = pd.read_csv(DATA_PATH.joinpath(decile))

        # Remove columns that we won't use:
        df = df.drop(["Code", "Major Food Code", "Minor Food Code", "RSE indicator(a)", "% change since 201516",
                      "sig(b)", "trend since 201516(c)"], axis=1)

        dec_df = preprocess_sheet(df)
        dec_df = dec_df.rename(columns={2019: "Décile " + str(i)})

        # get total to calculate others
        df_other = pd.read_csv(DATA_PATH.joinpath("total" + decile))

        total = df_other.iloc[11]["201819"]

        dec_df = dec_df["Décile " + str(i)]
        dec_df.loc["Other"] = total - dec_df.sum()

        dec_df = dec_df / 100  # convert to pounds

        res_df = pd.concat(
            [res_df, dec_df], axis=1)

    # Calculate percentages
    perc_df = res_df.copy(deep=True)
    cols = perc_df.columns.tolist()
    perc_df[cols] = perc_df[cols].div(
        perc_df[cols].sum(axis=0), axis=1).multiply(100)

    print("barchart done")

    return res_df, perc_df


def preprocess_map(regions):
    """
    Reads and prepares the data for the map.

    Returns:
        A dictionary with key being the region and value being the processed dataframe for that region
    """
    print("map")

    dict_of_dfs = {}

    for region in regions:
        df = pd.read_csv(DATA_PATH.joinpath(
            region.replace(" the ", " The ").replace(" ", "_")))

        newName = region.replace("The", "the")
        # Remove columns that we won't use:
        df = df.drop(["Code", "Major Food Code", "Minor Food Code", "RSE indicator(a)", "% change since 201516",
                      "sig(b)", "trend since 201516(c)"], axis=1)

        df = preprocess_sheet(df)

        dict_of_dfs[newName] = df

    # calculte mean for each category

    moy_df = pd.DataFrame()
    map_df = pd.DataFrame(index=list(dict_of_dfs.keys()),
                          columns=dict_of_dfs["London"].index)
    for sheet_name in dict_of_dfs:
        moy_df = pd.concat([moy_df, dict_of_dfs[sheet_name][2019]], axis=1)
        map_df.loc[sheet_name] = dict_of_dfs[sheet_name][2019]

    dict_of_dfs["moy2019"] = moy_df.mean(axis=1).to_frame().round(1)

    print("map done")
    return dict_of_dfs, map_df


def get_regions(regions_data):
    '''
        Gets the name of the regions in the dataset

        Args:
            regions_data: The data to parse
        Returns:
            locations: An array containing the names of the
                regions in the data set
    '''

    # converting to dataframe is easier to extract revelant data:
    my_df = pd.json_normalize(regions_data["features"])["properties.rgn19nm"]
    # return data as array:
    locations = my_df.to_numpy()

    # for the locations to match our geojson data
    for i in range(len(locations)):
        locations[i] = locations[i].replace("_", " ")

    return my_df.to_numpy()
