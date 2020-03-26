#! /usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import time

average_months = 12 #months
category = 'RTNG' #standard
top = 60 #players

norges_search = 'https://www.norgesratinga.no/?clubFilter=all&limit=1000000&period=MAR20&page=KadettA&flag=&search=&ratingType=&federation='

def average_FIDE(fide_id):
    html = requests.get(f'https://ratings.fide.com/profile/{fide_id}/chart')
    soup = BeautifulSoup(html.content, 'lxml')
    table = soup.findAll('table', {'class': 'profile-table profile-table_chart-table'})
    df = pd.read_html(str(table))[0]
    avg = df.head(average_months)[category].mean().round()

    player = soup.find('div', {'class': 'col-lg-8 profile-top-title'}).get_text()

    return player, avg

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
    p, a = average_FIDE(player)
    output[p] = a
    time.sleep(1)

for p, a in output.items():
    print(p, a)

