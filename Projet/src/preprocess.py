from matplotlib.pyplot import axis
import pandas as pd
import numpy as np

#! odfpy needs to be installed : pip install odfpy
try:
    import odf
except ModuleNotFoundError:
    print("odfpy needs to be installed: pip install odfpy")


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

    # Round the floats to 1 decimal place
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
    df = pd.read_excel("./assets/UKHHcons-27Jan2022.ods",
                       "Household_quantity", skiprows=7)  # skiprow 7 to skip all the titles and data

    # Remove columns that we won't use:
    df = df.drop(["Code", "Major Food Code", "Minor Food Code", "RSE(a)", "% change since 201617",
                  "% change since 201819", "sig(b)", "trend since 201617(c)"], axis=1)

    return preprocess_sheet(df)


def preprocess_bar_chart():
    """
    Reads and prepares the data for the bar chart.

    Returns:
        A dataframe containing quantities of different food categories for 1974 to 2020
    """

    res_df = pd.DataFrame()

    for i in range(1, 11):
        decile = "Decile_" + str(i)
        df = pd.read_excel("./assets/ConsEIDHH-29oct20.ods",
                           decile, skiprows=7)  # skiprow 7 to skip all the titles and data

        # Remove columns that we won't use:
        df = df.drop(["Code", "Major Food Code", "Minor Food Code", "RSE indicator(a)", "% change since 201516",
                      "sig(b)", "trend since 201516(c)"], axis=1)

        dec_df = preprocess_sheet(df)
        dec_df = dec_df.rename(columns={2019: "Décile " + str(i)})

        res_df = pd.concat(
            [res_df, dec_df["Décile " + str(i)].to_frame()], axis=1)

    #TODO: pourcentages


#!test:
preprocess_bar_chart()
