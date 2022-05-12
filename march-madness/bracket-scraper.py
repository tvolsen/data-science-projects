from bs4 import BeautifulSoup
import requests
import os
import csv

for year in range(2022, 2023):
    # skip the two years most heavily impacted by COVID-19 for stat reliability
    if year == 2020 or year == 2021:
        continue

    # HTML and CSV file names and paths
    url = f"https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/Bracket/{year}/"
    html_name = f"{year}-stats.html"
    html_file_path = f"brackets/{html_name}"
    csv_name = f"{year}-stats.csv"
    csv_file_path = f"brackets/{csv_name}"

    # only request if the file doesn't exist locally to prevent flooding the site
    if not os.path.exists(html_file_path):
        with open(html_file_path, "w") as f:
            response = requests.get(url)
            f.write(response.text)
        
    with open(html_file_path) as f:
        soup = BeautifulSoup(f, "html.parser")

    # find all of the relevant information from the HTML source
    all_games = soup.find_all(class_="bracket_game")
    all_games = [x.find_all(class_=["name", "score"]) for x in all_games]
    all_games = [[y.text for y in x] for x in all_games]
    results = []
    while all_games:
        game = all_games.pop(0)
        team0_name = game.pop(0)
        team0_score = int(game.pop(0))
        team1_name = game.pop(0)
        team1_score = int(game.pop(0))
        if team0_score > team1_score:
            results.append([year, team0_name, team1_name])
        else:
            results.append([year, team1_name, team0_name])
    print(results)


    # # save all of the information to a csv file
    # with open(csv_file_path, "w") as f:
    #     write = csv.writer(f)
    #     # here are the column headers
    #     categories = ["year", "school", "pts", "fgm", "fga", "3pm", "3pa", "ftm", "fta", "orb", "drb", "reb", "ast", "stl", "blk", "tov", "pf"]
    #     write.writerow(categories)
    #     while all_stats:
    #         team = []
    #         # add the year and school columns
    #         team.append(year)
    #         team.append(all_stats.pop(0).text)
    #         for i in range(20):
    #             # ignore a few irrelevant or incompatible columns
    #             if i in [0, 1, 5, 8, 11]:
    #                 all_stats.pop(0)
    #             else:
    #                 # format the numbers as integers
    #                 s = str(all_stats.pop(0).text)
    #                 s = s.replace(",", "")
    #                 team.append(int(s))
    #         write.writerow(team)