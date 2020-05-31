import re
from urllib.request import Request, urlopen
from flask import render_template


def anime_watch(anime_link):
    link = "https://www.animefreak.tv/watch/" + anime_link
    request = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(request).read().decode("utf-8")
    image = re.findall(r'src="(.*?)">', html)  # 4
    episodes_links = re.findall(r'<a href="(.*?)">', html)
    x = -1
    links = []
    while len(episodes_links) - 1 > x:
        x += 1
        if 'movie' in episodes_links[x]:
            if '/episode/movie' in episodes_links[x]:
                links.append(episodes_links[x])

        if anime_link + '/episode/episode' in episodes_links[x]:
            links.append(episodes_links[x])
    anime_name = re.findall(r'<div class="anime-title">(.*?)</div>', html)
    if '/episode/movie' in links[0]:
        links = ["movie"]
        return render_template('anime-watch-movie.html', image=image, links=links, anime_name=anime_name[0],
                               anime_link=anime_link)
    else:
        x = -1
        while len(links) - 1 > x:
            x += 1
            links[x] += str("code124245")
            str(links[x])
            links[x] = re.findall(r'' + str(link) + '/episode/episode-(.*?)code124245', links[x])[0]
        return render_template('anime-watch.html', image=image, links=links, anime_name=anime_name[0],
                               anime_link=anime_link)
