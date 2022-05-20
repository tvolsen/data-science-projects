from bs4 import BeautifulSoup
import requests
import os
import csv

# each bracket url has a different number at the end, since there is such a small number of brackets, I found manually copying them was the easiest option
url_year = {
    2003 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2003/312",
    2004 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2004/311",
    2005 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2005/310",
    2006 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2006/309",
    2007 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2007/230",
    2008 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2008/229",
    2009 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2009/227",
    2010 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2010/226",
    2011 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2011/433", 
    2012 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2012/489", 
    2013 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2013/546",
    2014 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2014/610",
    2015 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2015/677",
    2016 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2016/708",
    2017 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2017/803",
    2018 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2018/872",
    2019 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2019/936",
    2022 : "https://basketball.realgm.com/ncaa/tournaments/Post-Season/NCAA-Tournament/1/bracket/2022/1128"
}

for year in range(2003, 2023):
    # skip the two years most heavily impacted by COVID-19 for stat reliability
    if year == 2020 or year == 2021:
        continue

    # HTML and CSV file names and paths
    url = url_year[year]
    html_name = f"{year}-bracket.html"
    html_file_path = f"brackets/{html_name}"
    csv_name = f"{year}-bracket.csv"
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

    # save all of the information to a csv file
    with open(csv_file_path, "w") as f:
        write = csv.writer(f)
        # here are the column headers
        categories = ["year", "winner", "loser"]
        write.writerow(categories)
        while results:
            result = results.pop(0)
            write.writerow(result)