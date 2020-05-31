import sqlite3, requests, re 

def update_database_list():
    conn = sqlite3.connect("anime_database.db")
    c = conn.cursor()
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
    c.execute("SELECT * FROM list")
    anime_list = c.fetchall()
    for row in range(len(show_names)):
        if (show_names[row] == anime_list[row][0]) and (show_links_list[row] == anime_list[row][1]):
            pass
        else:
            c.execute("INSERT INTO list VALUES('"+ show_names[row] +"','"+ show_links_list[row] +"')") 
    conn.commit()
    conn.close()

def update_database_latest():
    conn = sqlite3.connect("anime_database.db")
    
    c = conn.cursor()

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
    c.execute("SELECT * FROM latest")
    latest = c.fetchall()
    for row in range(len(show_names)):
        if (latest[row][0] == show_names[row]) and (latest[row][1] == show_links[row]) and (latest[row][2] == covers_list[row]):
            pass
        else:
            c.execute("INSERT INTO latest VALUES ('"+ show_names[row] +"','"+ show_links[row] +"','"+ covers_list[row] +"')")
    conn.commit()
    conn.close()
