#! /usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import time

average_months = 12 #months
category = 'RTNG' #standard
games = "GMS" #standard games
top = 60 #players
max_b_year = 2004
min_b_year = 1997

norges_search = 'https://www.norgesratinga.no/?clubFilter=all&limit=1000000&period=MAR20&page=KadettA&flag=&search=&ratingType=&federation='

def average_FIDE(fide_id):
    html = requests.get(f'https://ratings.fide.com/profile/{fide_id}/chart')
    soup = BeautifulSoup(html.content, 'lxml')
    table = soup.findAll('table', {'class': 'profile-table profile-table_chart-table'})
    df = pd.read_html(str(table))[0]
    avg = df.head(average_months)[category].mean().round()
    count = df.head(average_months)[games].sum()

    player = soup.find('div', {'class': 'col-lg-8 profile-top-title'}).get_text()

    b_year_section = soup.find(text=re.compile('B-Year')).parent.parent.text
    b_year = int(re.search(r"\d+", b_year_section).group(0))
    if b_year > max_b_year or b_year < min_b_year:
        return None
    return player, avg, count

def get_Vikings(search):
    html = requests.get(search)
    soup = BeautifulSoup(html.content, 'lxml')
    players = []
    for ident in soup.findAll('tr', {'id': re.compile(r'KadettA-(\d+)')}):
        players.append(ident.get('id').split('-')[-1])
    return players

output = {}

players = get_Vikings(norges_search)

for player in players[:top]:
    vals = average_FIDE(player)
    if vals:
        p, a, c = vals
        output[p] = a, c
        time.sleep(1)
    else:
        continue

for p, vals in output.items():
    print(p, vals)

