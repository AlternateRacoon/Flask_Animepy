import re
from urllib.request import Request, urlopen
from anime_search_page import anime_search
from anime_watch_page import anime_watch
from anime_index_page import anime_index
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return anime_index()


@app.route('/watch/<anime_link>')
def watch(anime_link):
    return anime_watch(anime_link)


@app.route('/watch/<anime_link>/episode/<int:anime_episode>')
def episode(anime_link, anime_episode):
    url = str('https://www.animefreak.tv/watch/' + str(anime_link) + '/episode/episode-' + str(anime_episode))
    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(request).read().decode("utf-8")
    mp4_link = re.findall(r'var file = "(.*?)"', html)
    return render_template('anime-episode.html', link=mp4_link)


@app.route('/watch/<anime_link>/movie/movie')
def movie(anime_link):
    url = str('https://www.animefreak.tv/watch/' + str(anime_link) + '/episode/movie')
    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(request).read().decode("utf-8")
    mp4_link = re.findall(r'var file = "(.*?)"', html)
    return render_template('anime-episode.html', link=mp4_link)


@app.route('/search/<anime_name>')
def search(anime_name):
    return anime_search(anime_name)


@app.route('/about')
def about():
    return '<p>A Project that scrapes anime and is coded in python :3</p>'


@app.route('/contact')
def contact():
    return 'contacts about myself that i will add later'


@app.route('/animelist')
def animelist():
    return render_template('anime-list.html')


if __name__ == "__main__":

    app.run(host="0.0.0.0",port=80,debug=True)
