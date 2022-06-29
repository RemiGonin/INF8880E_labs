"""
This script converts all our ods files to csv prior to preprocessing, because reading csv is approx 100x faster than reading ods. 
Only used it 1 time to convert the data. It is not called anymore afterwards in the program.
"""

import pandas as pd
import pathlib


barchart_dfs = pd.read_excel("../data/ExpEID29oct20.ods",
                             sheet_name=None, engine="odf", skiprows=25)  # skiprow 25 to skip all the titles and data

total_df = pd.read_excel("../data/ExpEID29oct20.ods",
                         sheet_name=None, engine="odf", skiprows=7, nrows=16)  # Just get total


map_dfs = pd.read_excel("../data/ConsGORHH_29oct20.ods",
                        sheet_name=None, engine="odf", skiprows=7)  # skiprow 7 to skip all the titles and data

exp_df = pd.read_excel("../data/UKExp-27Jan2022.ods",
                       "expenditure", skiprows=24, engine='odf')  # skiprow 7 to skip all the titles and data


for sheetname in barchart_dfs:
    barchart_dfs[sheetname].to_csv(sheetname, index=False)

for sheetname in map_dfs:
    map_dfs[sheetname].to_csv(sheetname, index=False)

for sheetname in total_df:
    total_df[sheetname].to_csv("total" + sheetname, index=False)

exp_df.to_csv("expenditure", index=False)
