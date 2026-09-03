import html
from datetime import datetime
from posts import POSTS

def write_articles(dist, layout):
    rows = ''
    for post in POSTS:
        display = datetime.strptime(post['date'], '%Y-%m-%d').strftime('%d %b %Y')
        rows += ('<a class="post-row" href="/articles/' + post['slug'] + '/"><p class="date">' + display + '</p><h2>' + html.escape(post['title']) + '</h2><p>' + html.escape(post['deck']) + '</p></a>')
    index = ('<main class="wrap"><div class="page-hero"><p class="kicker">Notes</p><h1>Articles</h1><p class="lede">Quiet reading on pipeline, labour, packages and the numbers behind the week.</p></div><div class="post-list">' + rows + '</div></main>')
    path = dist / 'articles' / 'index.html'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(layout('Articles', '/articles/', 'Construction notes from Behind the Facade.', index), encoding='utf-8')
    for post in POSTS:
        display = datetime.strptime(post['date'], '%Y-%m-%d').strftime('%d %b %Y')
        others = ''
        for other in POSTS:
            if other['slug'] == post['slug']:
                continue
            od = datetime.strptime(other['date'], '%Y-%m-%d').strftime('%d %b %Y')
            others += '<a href="/articles/' + other['slug'] + '/"><span class="date">' + od + '</span> ' + html.escape(other['title']) + '</a>'
        essay = ('<main class="wrap"><article class="essay"><p class="date">' + display + ' - Behind the Facade</p><h1>' + html.escape(post['title']) + '</h1><p class="lede">' + html.escape(post['deck']) + '</p>' + post['body'] + '<div class="related"><p class="kicker">More notes</p>' + others + '</div></article></main>')
        dest = dist / 'articles' / post['slug'] / 'index.html'
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(layout(post['title'], '/articles/' + post['slug'] + '/', post['deck'], essay), encoding='utf-8')
