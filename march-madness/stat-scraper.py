from bs4 import BeautifulSoup
import requests
from os.path import exists
import csv

url = "https://basketball.realgm.com/ncaa/team-stats/2022/Totals/Team_Totals/0"
name = "2022.html"
file_path = f"stats/{name}"

if not exists(file_path):
    with open(file_path, "w") as f:
        response = requests.get(url)
        f.write(response.text)
        
with open(file_path) as f:
    soup = BeautifulSoup(f, "html.parser")

all_stats = soup.find_all(name="td", class_="")

with open("stats/2022.csv", "w") as f:
    write = csv.writer(f)
    categories = ["school", "pts", "fgm", "fga", "3pm", "3pa", "ftm", "fta", "orb", "drb", "reb", "ast", "stl", "blk", "tov", "pf"]
    write.writerow(categories)
    while all_stats:
        team = []
        team.append(all_stats.pop(0).text)
        for i in range(20):
            if i in [0, 1, 5, 8, 11]:
                all_stats.pop(0)
            else:
                s = str(all_stats.pop(0).text)
                s = s.replace(",", "")
                team.append(int(s))
        write.writerow(team)