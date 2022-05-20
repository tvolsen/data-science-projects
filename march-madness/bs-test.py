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

    rounds_dict = {
        "First Four" : 0,
        "Play In Game" : 0,
        "First Round" : 1,
        "Second Round" : 2,
        "Sweet Sixteen" : 3,
        "Elite Eight" : 4,
        "Final Four" : 5,
        "Championship Game" : 6
    }

    team_region = {}

    # find all of the relevant information from the HTML source
    bracket = soup.find(class_="bracket")
    # bracket = [x.find_all(class_=["round", "name", "score"]) for x in bracket]
    bracket = bracket.find_all(class_=["round", "name", "score"])
    # bracket = bracket[0]
    bracket = [y.text for y in bracket]

    results = []
    region_matchup = []

    while bracket:
        bracket[0] = bracket[0].split(" (")[0]
        if bracket[0] in rounds_dict:
            round = rounds_dict[bracket.pop(0)]
            if round in [0, 5, 6]:
                region = "none"
        elif "Region" in bracket[0]:
            region = bracket.pop(0)
        else:
            team0_name = bracket.pop(0)
            team0_score = int(bracket.pop(0))
            team1_name = bracket.pop(0)
            team1_score = int(bracket.pop(0))
            if team0_score > team1_score:
                results.append([year, team0_name, team1_name, region, round])
            else:
                results.append([year, team1_name, team0_name, region, round])
            if team0_name not in team_region and region != "none":
                team_region[team0_name] = region
            if team1_name not in team_region and region != "none":
                team_region[team1_name] = region
            if round == 5:
                region_matchup.append(team_region[team0_name])
                region_matchup.append(team_region[team1_name])
    # save all of the information to a csv file
    with open(csv_file_path, "w") as f:
        write = csv.writer(f)
        # here are the column headers
        categories = ["year", "winner", "loser", "region", "round"]
        write.writerow(categories)
        while results:
            result = results.pop(0)
            write.writerow(result)
        write.writerow(region_matchup)