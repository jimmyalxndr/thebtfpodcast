import html
from site_config import SHOW, SITE

FONTS = 'https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Outfit:wght@300;400;600&family=Syne:wght@700&display=swap'

def layout(title, path, description, body, image='/cover.jpg'):
    abs_img = image if image.startswith('http') else SITE + image
    page = title if title == SHOW['title'] else title + ' | ' + SHOW['title']
    return (
        '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>' + html.escape(page) + '</title>'
        '<meta name="description" content="' + html.escape(description) + '">'
        '<link rel="canonical" href="' + SITE + path + '">'
        '<link rel="icon" href="/cover.jpg">'
        '<link href="' + FONTS + '" rel="stylesheet">'
        '<meta property="og:title" content="' + html.escape(title) + '">'
        '<meta property="og:image" content="' + html.escape(abs_img) + '">'
        '<link rel="stylesheet" href="/styles.css"></head><body>'
        '<header id="top"><div class="wrap nav">'
        '<a class="brand" href="/"><img src="/cover.jpg" alt="">Behind the Facade</a>'
        '<button class="menu-toggle" type="button" onclick="document.getElementById(\'top\').classList.toggle(\'open\')">Menu</button>'
        '<nav><a href="/episodes/">Episodes</a><a href="/articles/">Articles</a>'
        '<a href="/hosts/">Hosts</a><a href="/guests/">Guests</a>'
        '<a href="/pitch/">Be a guest</a>'
        '<a href="' + SHOW['youtube'] + '" target="_blank" rel="noreferrer">YouTube</a></nav>'
        '</div></header>'
        + body +
        '<footer><div class="wrap foot"><div>'
        '<strong style="color:var(--cream);font-family:Instrument Serif,serif;font-size:28px;font-weight:400">Behind the Facade</strong>'
        '<div>Melbourne construction. The conversations behind the work.</div>'
        '<div class="foot-links"><a href="' + SHOW['spotify'] + '">Spotify</a><a href="' + SHOW['apple'] + '">Apple</a>'
        '<a href="' + SHOW['youtube'] + '">YouTube</a><a href="/feed">RSS</a>'
        '<a href="mailto:contact@thebtfpodcast.com">contact@thebtfpodcast.com</a></div></div>'
        '<form class="subscribe" name="subscribe" method="POST" data-netlify="true" netlify-honeypot="bot-field">'
        '<input type="hidden" name="form-name" value="subscribe">'
        '<p style="display:none"><label>Do not fill this out <input name="bot-field"></label></p>'
        '<label>Subscribe to the list<span class="sub-row">'
        '<input type="email" name="email" required placeholder="Email address">'
        '<button class="btn" type="submit">Join</button></span></label>'
        '<p class="sub-note">Episodes and notes. No noise.</p></form></div></footer></body></html>'
    )

def render_home(latest, rest, hosts, guests, count):
    bg = html.escape(latest['image'])
    yt = SHOW['youtube']
    guest_cards = ''
    for g in guests[:4]:
        guest_cards += (
            '<a class="card" href="/guests/"><img src="/thumbs/' + g['episode'] + '.jpg" alt="">'
            '<div class="body"><p class="meta">Episode ' + html.escape(g['episode']) + '</p>'
            '<h3>' + html.escape(g['name']) + '</h3><p>' + html.escape(g['summary']) + '</p></div></a>'
        )
    return (
        '<main>'
        '<section class="stage"><div class="stage-bg" style="background-image:url(\'' + bg + '\')"></div>'
        '<div class="stage-shade"></div><div class="wrap stage-copy">'
        '<p class="kicker">Melbourne construction podcast</p>'
        '<h1>Behind <em>the</em> Facade</h1>'
        '<p class="lede">' + html.escape(SHOW['tagline']) + '</p>'
        '<div class="btns"><a class="btn" href="/episodes/' + latest['slug'] + '/">Watch the latest</a>'
        '<a class="btn ghost" href="' + yt + '" target="_blank" rel="noreferrer">YouTube</a>'
        '<a class="btn ghost" href="' + SHOW['spotify'] + '" target="_blank" rel="noreferrer">Spotify</a></div>'
        '</div></section>'
        '<div class="stats">'
        '<div class="stat"><b>' + str(count) + '</b><span>Episodes on record</span></div>'
        '<div class="stat"><b>Melbourne</b><span>Built on site, not in a studio farm</span></div>'
        '<div class="stat"><b>Jake + Daniel</b><span>Proline and Complex Facade</span></div>'
        '<div class="stat"><b>Fortnightly</b><span>The conversations behind the work</span></div>'
        '</div>'
        '<p class="marquee">Facades · Cladding · Glass · Labour · Programmes · Data centres · Hospitals · Housing · The work itself · </p>'
        '<section class="wrap"><div class="section-head"><h2>Now playing</h2><a href="/episodes/">All episodes</a></div>'
        '<article class="featured"><a class="featured-media" href="/episodes/' + latest['slug'] + '/">'
        '<img src="' + bg + '" alt=""><span class="play-badge">Play episode ' + html.escape(latest['episode']) + '</span></a>'
        '<div class="featured-copy"><p class="meta">Episode ' + html.escape(latest['episode']) + ' · ' + html.escape(latest['dateLabel']) + ' · ' + html.escape(latest['duration']) + '</p>'
        '<h3><a href="/episodes/' + latest['slug'] + '/">' + html.escape(latest['title']) + '</a></h3>'
        '<p class="lede" style="margin-bottom:22px">' + html.escape(latest['excerpt']) + '</p>'
        '<div class="btns"><a class="btn" href="/episodes/' + latest['slug'] + '/">Read and play</a>'
        '<a class="btn ghost" href="' + yt + '" target="_blank" rel="noreferrer">Watch on YouTube</a></div></div></article></section>'
        '<section class="wrap"><div class="section-head"><h2>The archive</h2><a href="/episodes/">See every conversation</a></div>'
        '<div class="grid">' + ''.join(
            '<a class="card" href="/episodes/' + e['slug'] + '/"><img src="' + html.escape(e['image']) + '" alt="">'
            '<div class="body"><p class="meta">Ep ' + html.escape(e['episode']) + ' · ' + html.escape(e['duration']) + '</p>'
            '<h3>' + html.escape(e['title']) + '</h3></div></a>' for e in rest
        ) + '</div></section>'
        '<section class="wrap"><div class="section-head"><h2>The hosts</h2><a href="/hosts/">Full bios</a></div><div class="split">'
        '<div class="host"><p class="kicker">Host</p><h3>Jake Gorry</h3><p>' + html.escape(hosts[0]['summary']) + '</p><a class="btn ghost" href="/hosts/">Jake</a></div>'
        '<div class="host"><p class="kicker">Host</p><h3>Daniel Alizzi</h3><p>' + html.escape(hosts[1]['summary']) + '</p><a class="btn ghost" href="/hosts/">Daniel</a></div>'
        '</div></section>'
        '<section class="wrap"><div class="section-head"><h2>Guests</h2><a href="/guests/">All guests</a></div>'
        '<div class="grid">' + guest_cards + '</div></section>'
        '</main>'
    )
