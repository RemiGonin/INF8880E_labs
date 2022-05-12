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
    PlayerLine = my_df.groupby(["Act", "Player"]).agg("sum")[
        "Line"].rename("LineCount")

    SumLinesPerAct = my_df.groupby(["Act"]).agg("sum")["Line"]
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

    # Count Line
    Top5Count = my_df.groupby(level='Act')['LineCount'].nlargest(
        5).reset_index(level=0, drop=True)
    print(type(Top5Count))
    SumTop5Count = Top5Count.groupby(["Act"]).sum()
    SumCountOthers = my_df.groupby(["Act"]).agg(
        "sum")["LineCount"] - SumTop5Count
    SumCountOthers = pd.concat([SumCountOthers], keys=[
                               'OTHERS'], names=['Player']).swaplevel(0, 1)

    Top6Count = Top5Count.append(SumCountOthers)
    Top6Count = Top6Count.groupby(level=0).apply(
        lambda x: x.reset_index(level="Act", drop=True))

    # Count Percent
    Top5Percent = my_df.groupby(level='Act')['LinePercent'].nlargest(
        5).reset_index(level=0, drop=True)
    SumTop5Percent = Top5Percent.groupby(["Act"]).sum()
    SumPercentOthers = my_df.groupby(["Act"]).agg(
        "sum")["LinePercent"] - SumTop5Percent
    SumPercentOthers = pd.concat([SumPercentOthers], keys=[
        'OTHERS'], names=['Player']).swaplevel(0, 1)

    Top6Percent = Top5Percent.append(SumPercentOthers)
    Top6Percent = Top6Percent.groupby(level=0).apply(
        lambda x: x.reset_index(level="Act", drop=True))

    my_df = pd.concat([Top6Count, Top6Percent],
                      axis=1)
    # my_df = my_df.groupby(["Act"])
    print(my_df.to_string())
    return my_df


def clean_names(my_df):
    '''
        In the dataframe, formats the players'
        names so each word start with a capital letter.

        Returns:
            The df with formatted names
    '''
    # TODO : Clean the player names
    my_df["Player"] = my_df["Player"].str.capitalize()
    print(my_df)
    return my_df
