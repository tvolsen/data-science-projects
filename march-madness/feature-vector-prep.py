# basic imports
import pandas as pd
import numpy as np

all_stats = pd.read_csv("all_stats.csv")

# create a dataframe of each tournament game
df_games = pd.DataFrame({})
for year in range(2003, 2023):
    if year == 2020 or year == 2021:
        continue
    df_bracket = pd.read_csv(f"brackets/{year}-bracket.csv")
    df_bracket = df_bracket[df_bracket["round"] > 0]
    year_stats = all_stats[all_stats["year"] == year]
    for i, game in df_bracket.iterrows():
        teams = [game.team0, game.team1]
        teams_df = year_stats[year_stats["team"].isin(teams)]
        if len(teams_df) < 2:
            continue
        team0 = teams_df.iloc[0].drop(["year", "team"])
        team1 = teams_df.iloc[1].drop(["year", "team"])
        
        team0_team1 = team0 - team1
        team0_team1["year"] = game.year
        team0_team1["team0"] = game.team0
        team0_team1["team1"] = game.team1
        
        team1_team0 = team1 - team0
        team1_team0["year"] = game.year
        team1_team0["team0"] = game.team1
        team1_team0["team1"] = game.team0
        if np.isnan(game.winner):
            team0_team1["result"] = np.nan
            team1_team0["result"] = np.nan
        else:
            team0_team1["result"] = game.winner
            team1_team0["result"] = 1 - game.winner
        
        df_games = df_games.append(team0_team1, ignore_index=True)
        df_games = df_games.append(team1_team0, ignore_index=True)

df_games = df_games.round(3)
df_games.to_csv("input-vectors.csv", index=False)