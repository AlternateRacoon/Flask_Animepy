import re
import sqlite3
from urllib.request import Request, urlopen
from get_anime_database import get_database_list
from flask import render_template

def anime_search(anime_name):
    anime_list = []
    for row in get_database_list():
        anime_list.append(str(row[1]))
    anime_name = anime_name.lower()
    if len(anime_name.split()) == 2:
        anime_name = anime_name.split()[0] + "-" + anime_name.split()[1]
    if len(anime_name.split()) == 3:
        anime_name = anime_name.split()[0] + "-" + anime_name.split()[1] + "-" + anime_name.split()[2]
    if len(anime_name.split()) == 4:
        anime_name = anime_name.split()[0] + "-" + anime_name.split()[1] + "-" + anime_name.split()[2] + "-" + \
                     anime_name.split()[3]
    matching = [s for s in anime_list if anime_name in s]
    filtered_list = []
    for row in matching:
        conn = sqlite3.connect("anime_database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM list WHERE link='" + row + "'")
        filtered_list.append(c.fetchone())
        conn.commit()
        conn.close()

    photos = []
    for row in range(len(filtered_list)):
        if 'https://www.animefreak.tv/watch/' in filtered_list[row][1]:
            url = str(filtered_list[row][1])
        else:
            url = str('https://www.animefreak.tv/watch/' + filtered_list[row][1])
        request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(request).read().decode("utf-8")
        cover_photo = re.findall('" src="(.*?)">', html)
        photos.append(cover_photo[0])

    return render_template('index-search.html', list=filtered_list, photos=photos)
