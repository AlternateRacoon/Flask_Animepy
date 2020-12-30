import re
import sqlite3
from urllib.request import Request, urlopen
from flask import render_template
from update_anime_database import update_database_latest


def anime_index():
    request = Request("https://www.animefreak.tv/", headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(request).read().decode("utf-8")
    show_names = re.findall('" class="nli-serie">(.*?)</a>', html)
    shows_latest = []
    for row in range(len(show_names)):
        conn = sqlite3.connect("anime_database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM latest WHERE name='" + show_names[row] + "'")
        show = c.fetchone()
        if show == None:
            update_database_latest()
        else:
            shows_latest.append(show)
        conn.commit()
        conn.close()
    latest_shows = []
    for row in shows_latest:
        if "https://www.animefreak.tv/watch/" in row[1]:
            stuff = row[1] + "code6969"
            link = re.findall('/watch/(.*?)code6969', stuff)
            latest_shows.append([row[0], link[0], row[2]])
        else:
            latest_shows.append(row[0], row[1], row[2])

    return render_template('index.html', latest=latest_shows)
