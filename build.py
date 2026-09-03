#!/usr/bin/env python3
from __future__ import annotations
import html, re, shutil, urllib.parse, urllib.request
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET
from site_config import COVER_URL, ITUNES, RSS_URL, SHOW, SITE
from content import ARTICLES, GUESTS, HOSTS, YOUTUBE
from thumbs import pull_thumb

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'dist'
CSS = (ROOT / 'styles.css').read_text(encoding='utf-8')

def slugify(title, episode):
    cleaned = re.sub(r'^#?\d+\s*-\s*', '', title.lower())
    cleaned = re.sub(r'[^a-z0-9]+', '-', cleaned).strip('-')[:80]
    return (episode + '-' + cleaned) if episode else cleaned

def plain(raw):
    text = re.sub(r'<[^>]+>', ' ', raw or '')
    return re.sub(r'\s+', ' ', html.unescape(text)).strip()

def excerpt(text, n=180):
    if len(text) <= n:
        return text
    return text[:n].rsplit(' ', 1)[0] + '...'

def duration(seconds):
    try:
        s = int(float(seconds))
    except Exception:
        return ''
    hours, minutes = divmod(s, 3600)
    minutes, _ = divmod(minutes, 60)
    return (str(hours) + 'h ' + f'{minutes:02d}m') if hours else (str(minutes) + ' min')

def date_label(rfc):
    try:
        return datetime.strptime((rfc or '')[:25], '%a, %d %b %Y %H:%M:%S').strftime('%d %b %Y')
    except Exception:
        return rfc or ''

def fetch():
    req = urllib.request.Request(RSS_URL, headers={'User-Agent': 'thebtfpodcast-site/1.0'})
    with urllib.request.urlopen(req, timeout=30) as res:
        root = ET.fromstring(res.read())
    out = []
    for item in root.find('channel').findall('item'):
        title = (item.findtext('title') or 'Untitled').strip()
        ep = (item.findtext(ITUNES + 'episode') or '').strip()
        desc = item.findtext('description') or ''
        enc = item.find('enclosure')
        img = item.find(ITUNES + 'image')
        article = ARTICLES.get(ep, {})
        out.append({
            'title': title,
            'episode': ep,
            'slug': slugify(title, ep),
            'dateLabel': date_label(item.findtext('pubDate')),
            'duration': duration(item.findtext(ITUNES + 'duration') or '0'),
            'audioUrl': enc.get('url') if enc is not None else '',
            'rssImage': img.get('href') if img is not None else '/cover.jpg',
            'image': '/cover.jpg',
            'descriptionHtml': desc,
            'excerpt': article.get('deck') or excerpt(plain(desc)),
            'article': article,
            'youtube': YOUTUBE.get(ep, ''),
        })
    return out

def put(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')

def buttons(compact=False):
    extra = '' if compact else '<a class="btn ghost" href="' + SHOW['rss'] + '" target="_blank" rel="noreferrer">RSS</a>'
    return ('<div class="btns"><a class="btn" href="' + SHOW['youtube'] + '" target="_blank" rel="noreferrer">YouTube</a><a class="btn ghost" href="' + SHOW['spotify'] + '" target="_blank" rel="noreferrer">Spotify</a><a class="btn ghost" href="' + SHOW['apple'] + '" target="_blank" rel="noreferrer">Apple</a>' + extra + '</div>')

def card(ep):
    return ('<a class="card" href="/episodes/' + ep['slug'] + '/"><img src="' + html.escape(ep['image']) + '" alt=""><div class="body"><p class="meta">Ep ' + html.escape(ep['episode']) + ' - ' + html.escape(ep['duration']) + '</p><h3>' + html.escape(ep['title']) + '</h3></div></a>')

def layout(title, path, description, body, image='/cover.jpg'):
    abs_img = image if image.startswith('http') else SITE + image
    page = title if title == SHOW['title'] else title + ' | ' + SHOW['title']
    return ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>' + html.escape(page) + '</title><meta name="description" content="' + html.escape(description) + '"><link rel="canonical" href="' + SITE + path + '"><link rel="icon" href="/cover.jpg"><link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&display=swap" rel="stylesheet"><meta property="og:title" content="' + html.escape(title) + '"><meta property="og:image" content="' + html.escape(abs_img) + '"><link rel="stylesheet" href="/styles.css"></head><body><header><div class="wrap nav"><a class="brand" href="/"><img src="/cover.jpg" alt="">Behind the Facade</a><nav><a href="/episodes/">Episodes</a><a href="/hosts/">Hosts</a><a href="/guests/">Guests</a><a href="/pitch/">Be a guest</a><a href="' + SHOW['youtube'] + '" target="_blank" rel="noreferrer">YouTube</a></nav></div></header>' + body + '<footer><div class="wrap foot"><div><strong style="color:#fff">Behind the Facade</strong><div>Melbourne construction podcast - Jake Gorry and Daniel Alizzi</div></div><div><a href="' + SHOW['spotify'] + '">Spotify</a><a href="' + SHOW['apple'] + '">Apple</a><a href="' + SHOW['youtube'] + '">YouTube</a><a href="/feed">RSS</a></div></div></footer></body></html>')

def article_html(ep):
    art = ep.get('article') or {}
    parts = []
    if art.get('kicker'):
        parts.append('<p class="kicker">' + html.escape(art['kicker']) + '</p>')
    if art.get('headline'):
        parts.append('<h2>' + html.escape(art['headline']) + '</h2>')
    if art.get('body'):
        parts.append('<div class="article">' + art['body'] + '</div>')
    takes = art.get('takeaways') or []
    if takes:
        items = ''.join('<li>' + html.escape(t) + '</li>' for t in takes)
        parts.append('<div class="article"><h2>From this episode</h2><ul>' + items + '</ul></div>')
    return ''.join(parts)

def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    req = urllib.request.Request(COVER_URL, headers={'User-Agent': 'thebtfpodcast-site/1.0'})
    with urllib.request.urlopen(req, timeout=30) as res:
        (DIST / 'cover.jpg').write_bytes(res.read())
    (DIST / 'styles.css').write_text(CSS, encoding='utf-8')
    episodes = fetch()
    thumbs = DIST / 'thumbs'
    thumbs.mkdir()
    for ep in episodes:
        dest = thumbs / (ep['episode'] + '.jpg')
        if ep['youtube'] and pull_thumb(ep['youtube'], dest):
            ep['image'] = '/thumbs/' + ep['episode'] + '.jpg'
        else:
            ep['image'] = ep.get('rssImage') or '/cover.jpg'
    latest, rest = episodes[0], episodes[1:7]
    guest_cards = ''
    for g in GUESTS:
        guest_cards += ('<div class="host"><img src="/thumbs/' + g['episode'] + '.jpg" alt=""><p class="kicker">Episode ' + html.escape(g['episode']) + '</p><h3>' + html.escape(g['name']) + '</h3><p>' + html.escape(g['summary']) + '</p><a class="btn ghost" href="/guests/">Read the write-up</a></div>')
    home = ('<main><section class="wrap hero"><img class="hero-art" src="/cover.jpg" alt=""><div><p class="kicker">Construction podcast - Melbourne - @BehindTheFacadeShow</p><h1>Behind<br>the Facade</h1><p class="lede">' + SHOW['tagline'] + '</p>' + buttons() + '</div></section><section class="wrap"><div class="section-head"><h2>Latest episode</h2><a href="/episodes/">All episodes</a></div><article class="latest"><img src="' + html.escape(latest['image']) + '" alt=""><div><p class="meta">Episode ' + html.escape(latest['episode']) + ' - ' + html.escape(latest['dateLabel']) + ' - ' + html.escape(latest['duration']) + '</p><h3><a href="/episodes/' + latest['slug'] + '/">' + html.escape(latest['title']) + '</a></h3><p>' + html.escape(latest['excerpt']) + '</p><div class="btns"><a class="btn" href="/episodes/' + latest['slug'] + '/">Read and play</a><a class="btn ghost" href="' + SHOW['youtube'] + '" target="_blank" rel="noreferrer">Watch on YouTube</a></div></div></article></section><section class="wrap"><div class="section-head"><h2>Recent</h2></div><div class="grid">' + ''.join(card(e) for e in rest) + '</div></section><section class="wrap"><div class="section-head"><h2>The hosts</h2><a href="/hosts/">Full bios</a></div><div class="split"><div class="host"><p class="kicker">Host</p><h3>Jake Gorry</h3><p>' + html.escape(HOSTS[0]['summary']) + '</p><a class="btn ghost" href="/hosts/">Jake</a></div><div class="host"><p class="kicker">Host</p><h3>Daniel Alizzi</h3><p>' + html.escape(HOSTS[1]['summary']) + '</p><a class="btn ghost" href="/hosts/">Daniel</a></div></div></section><section class="wrap"><div class="section-head"><h2>Guests</h2><a href="/guests/">All guests</a></div><div class="split">' + guest_cards + '</div></section></main>')
    put(DIST / 'index.html', layout(SHOW['title'], '/', SHOW['description'], home))
    archive = ('<main class="wrap"><div class="page-hero"><p class="kicker">Archive</p><h1>Episodes</h1><p class="lede">Every conversation as a long-form note, with audio on this site and video on YouTube.</p></div><div class="grid" style="padding-bottom:64px">' + ''.join(card(e) for e in episodes) + '</div></main>')
    put(DIST / 'episodes/index.html', layout('Episodes', '/episodes/', 'Every episode of Behind the Facade.', archive))
    for ep in episodes:
        yt = ''
        if ep['youtube']:
            yt = '<div class="yt"><iframe src="https://www.youtube.com/embed/' + ep['youtube'] + '" title="YouTube" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div>'
        audio = ''
        if ep['audioUrl']:
            audio = '<audio controls preload="none" src="' + html.escape(ep['audioUrl']) + '"></audio>'
        headline = (ep['article'] or {}).get('headline') or ep['title']
        body = ('<main class="wrap"><div class="page-hero"><p class="kicker">Episode ' + html.escape(ep['episode']) + ' - ' + html.escape(ep['dateLabel']) + ' - ' + html.escape(ep['duration']) + '</p><h1>' + html.escape(headline) + '</h1><p class="lede">' + html.escape(ep['excerpt']) + '</p></div>' + yt + audio + '<article class="ep"><aside><img src="' + html.escape(ep['image']) + '" alt="">' + buttons(True) + '</aside><div>' + article_html(ep) + '<div class="article"><h2>Show notes</h2><div class="notes">' + ep['descriptionHtml'] + '</div></div></div></article></main>')
        put(DIST / 'episodes' / ep['slug'] / 'index.html', layout(headline, '/episodes/' + ep['slug'] + '/', ep['excerpt'], body, ep['image']))
    host_blocks = ''
    for h in HOSTS:
        host_blocks += ('<article class="panel" style="margin-bottom:20px"><p class="kicker">' + html.escape(h['role']) + '</p><h2 style="text-transform:uppercase;margin:0 0 12px">' + html.escape(h['name']) + '</h2>' + h['body'] + '<div class="btns"><a class="btn ghost" href="' + h['linkedin'] + '" target="_blank" rel="noreferrer">LinkedIn</a><a class="btn ghost" href="' + h['company_url'] + '" target="_blank" rel="noreferrer">' + html.escape(h['company']) + '</a></div></article>')
    about = ('<main class="wrap" style="padding-bottom:72px"><div class="page-hero"><p class="kicker">The show</p><h1>Jake and Daniel</h1><p class="lede">' + html.escape(SHOW['description']) + '</p></div>' + host_blocks + '</main>')
    put(DIST / 'hosts/index.html', layout('Hosts', '/hosts/', 'Jake Gorry and Daniel Alizzi, hosts of Behind the Facade.', about))
    put(DIST / 'about/index.html', layout('About', '/about/', SHOW['description'], about))
    guest_blocks = ''
    for g in GUESTS:
        guest_blocks += ('<article class="guest-card"><div><img src="/thumbs/' + g['episode'] + '.jpg" alt=""><p class="badge">Episode ' + html.escape(g['episode']) + '</p><h2 style="margin:0 0 8px;text-transform:uppercase">' + html.escape(g['name']) + '</h2><p class="meta">' + html.escape(g['title']) + ' - ' + html.escape(g['company']) + '</p></div><div>' + g['body'] + '<div class="btns"><a class="btn" href="/episodes/">Find the episode</a><a class="btn ghost" href="' + g['url'] + '" target="_blank" rel="noreferrer">Company</a><a class="btn ghost" href="' + g['linkedin'] + '" target="_blank" rel="noreferrer">LinkedIn</a></div></div></article>')
    guests_page = ('<main class="wrap" style="padding-bottom:72px"><div class="page-hero"><p class="kicker">The list</p><h1>Guests</h1><p class="lede">The contractors, founders and operators who have sat down with Jake and Daniel so far.</p></div><div class="guest-grid">' + guest_blocks + '</div></main>')
    put(DIST / 'guests/index.html', layout('Guests', '/guests/', 'Guests of Behind the Facade.', guests_page))
    pitch = ('<main class="wrap" style="padding-bottom:72px"><div class="page-hero"><p class="kicker">Bookings</p><h1>Be a guest</h1><p class="lede">If you run a construction business, lead a trade, or have a story that is actually useful on site, send it through.</p></div><form name="guest" method="POST" data-netlify="true" netlify-honeypot="bot-field"><input type="hidden" name="form-name" value="guest"><p style="display:none"><label>Do not fill this out <input name="bot-field"></label></p><label>Name <input type="text" name="name" required></label><label>Email <input type="email" name="email" required></label><label>Company / role <input type="text" name="company"></label><label>Why this conversation <textarea name="pitch" required></textarea></label><button class="btn" type="submit">Send pitch</button></form></main>')
    put(DIST / 'pitch/index.html', layout('Be a guest', '/pitch/', 'Pitch a guest for Behind the Facade.', pitch))
    print('Built', len(episodes), 'episodes')

if __name__ == '__main__':
    build()
