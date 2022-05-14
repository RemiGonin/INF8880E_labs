'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd
from modes import MODE_TO_COLUMN


def summarize_lines(my_df):
    '''
        Sums each player's total of number of lines and  its
        corresponding percentage per act.

        The sum of lines per player per act is in a new
        column named 'PlayerLine'.

        The percentage of lines per player per act is
        in a new column named 'PlayerPercent'

        Args:
            my_df: The pandas dataframe containing the data from the .csv file
        Returns:
            The modified pandas dataframe containing the
            information described above.
    '''
    # TODO : Modify the dataframe, removing the line content and replacing
    # it by line count and percent per player per act
    PlayerLine = my_df.groupby(["Act", "Player"]).size().rename("LineCount")

    SumLinesPerAct = my_df.groupby(["Act"]).size()
    PlayerPercent = 100 * PlayerLine / SumLinesPerAct
    PlayerPercent = PlayerPercent.rename("LinePercent")

    my_df = pd.concat([PlayerLine, PlayerPercent], axis=1)
    return my_df


def replace_others(my_df):
    '''
        For each act, keeps the 5 players with the most lines
        throughout the play and groups the other players
        together in a new line where :

        - The 'Act' column contains the act
        - The 'Player' column contains the value 'OTHER'
        - The 'LineCount' column contains the sum
            of the counts of lines in that act of
            all players who are not in the top
            5 players who have the most lines in
            the play
        - The 'PercentCount' column contains the sum
            of the percentages of lines in that
            act of all the players who are not in the
            top 5 players who have the most lines in
            the play

        Returns:
            The df with all players not in the top
            5 for the play grouped as 'OTHER'
    '''
    # TODO : Replace players in each act not in the top 5 by a
    # new player 'OTHER' which sums their line count and percentage

    # get the 5 players with largest number of lines in the whole play:
    Top5Count = my_df.groupby(["Player"]).sum().nlargest(
        5, "LineCount").drop("LinePercent", axis=1)

    # get the number of lines of those 5 players in each act:
    LinesInCommon = my_df.index.droplevel("Act").isin(
        Top5Count.index)
    Top5CountPerAct = my_df.loc[LinesInCommon]

    # To count the # of lines of other players in each act, we count the number of lines of all others players in each act
    LinesNotInCommon = [not elem for elem in LinesInCommon]
    CountOthersPerAct = my_df.loc[LinesNotInCommon].groupby("Act").sum()[
        "LineCount"]
    CountOthersPerAct = pd.concat([CountOthersPerAct], keys=[
        'OTHERS'], names=['Player']).swaplevel(0, 1).to_frame()

    # To get the percentages, we substract the percentages of the top 5 players from 100 in each act
    PercentOthersPerAct = 100 - \
        Top5CountPerAct.groupby(["Act"]).sum()["LinePercent"]
    PercentOthersPerAct = pd.concat([PercentOthersPerAct], keys=[
        'OTHERS'], names=['Player']).swaplevel(0, 1).to_frame()

    # Append together Count and Percent calculations of other players in each act
    OthersPercentAndCount = CountOthersPerAct.append(
        PercentOthersPerAct).groupby("Act").sum()
    OthersPercentAndCount = pd.concat([OthersPercentAndCount], keys=[
        'OTHERS'], names=['Player']).swaplevel(0, 1)

    # Append everything together
    Top6CountAndPercent = Top5CountPerAct.append(OthersPercentAndCount)
    Top6CountAndPercent = Top6CountAndPercent.groupby(level=0).apply(
        lambda x: x.reset_index(level="Act", drop=True))

    my_df = Top6CountAndPercent

    return my_df


def clean_names(my_df):
    '''
        In the dataframe, formats the players'
        names so each word start with a capital letter.

        Returns:
            The df with formatted names
    '''
    # TODO : Clean the player names
    my_df = my_df.reset_index(level=1)
    my_df["Player"] = my_df["Player"].str.capitalize()
    return my_df
