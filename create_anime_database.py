import sqlite3

import requests
import re

def create_database_list():
    request = requests.get('https://www.animefreak.tv/home/anime-list', headers={'User-Agent': 'Mozilla/5.0'})

    html_data = request.content.decode("utf-8")
    show_links = re.findall(r'<li><a href="(.*?)"', html_data)

    show_links_list = []
    show_names = []
    for row in show_links:
        if '/watch/' in row:
            if 'episode' not in row:
                show_links_list.append(row)
    for row in show_links_list:
        show_name = re.findall(r' <li><a href="'+ row +'">(.*?)</a></li>', html_data)
        show_names.append(show_name[0])



    conn = sqlite3.connect("anime_database.db")

    c = conn.cursor()

    anime_list ="""
        CREATE TABLE list (
            name text NOT NULL,
            link text NOT NULL)"""
    c.execute(anime_list)
    for row in range(len(show_names)):
        link =  show_links_list[row] + "code6969"
        link_list = re.findall('/watch/(.*?)code6969', link)
        c.execute("INSERT INTO list VALUES('"+ show_names[row] +"','"+ link_list[0] +"')")
    conn.commit()
    conn.close()
def create_database_latest():
    request = requests.get('https://www.animefreak.tv', headers={'User-Agent': 'Mozilla/5.0'})

    html_data = request.content.decode("utf-8")
    show_links = re.findall('<a href="(.*?)" class="nli-serie">', html_data)
    show_names = re.findall('" class="nli-serie">(.*?)</a>', html_data)
    covers = re.findall('" src="(.*?)">', html_data)

    covers_list = []

    for row in covers:
        if '/meta/anime/' in row:
            covers_list.append(row)
        elif 'https://www.animefreak.tv/img/cover.jpg' in row:
            covers_list.append(row)

    conn = sqlite3.connect("anime_database.db")

    c = conn.cursor()

    anime_latest = """
        CREATE TABLE latest (
            name text NOT NULL,
            link text NOT NULL,
            cover text NOT NULL)"""
    c.execute(anime_latest)
    for row in range(len(show_names)):
        link =  show_links[row] + "code6969"
        link_list = re.findall('/watch/(.*?)code6969', link)
        c.execute("INSERT INTO latest VALUES('"+ show_names[row] +"','"+ link_list[0] +"','"+ covers_list[row] +"')")
    conn.commit()
    conn.close()
