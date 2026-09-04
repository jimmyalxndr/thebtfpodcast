import html
from site_config import SHOW, SITE

FONTS = 'https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Syne:wght@700&display=swap'
HERO = '/hero.jpg'
FALLBACK = 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=2000&q=80'

def layout(title, path, description, body, image='/cover.jpg'):
    abs_img = image if image.startswith('http') else SITE + image
    page = title if title == SHOW['title'] else title + ' | ' + SHOW['title']
    top = ' is-home' if path == '/' else ''
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
        '<link rel="stylesheet" href="/styles.css"></head><body class="' + top.strip() + '">'
        '<header id="top"><div class="wrap nav">'
        '<a class="brand" href="/"><img src="/cover.jpg" alt=""><span>Behind the Facade</span></a>'
        '<button class="menu-toggle" type="button" onclick="document.getElementById(\'top\').classList.toggle(\'open\')">Menu</button>'
        '<nav><a href="/episodes/">Episodes</a><a href="/articles/">Articles</a>'
        '<a href="/hosts/">Hosts</a><a href="/guests/">Guests</a>'
        '<a href="/pitch/">Be a guest</a>'
        '<a class="nav-cta" href="' + SHOW['youtube'] + '" target="_blank" rel="noreferrer">Watch</a></nav>'
        '</div></header>'
        + body +
        '<footer><div class="wrap foot"><div>'
        '<strong class="foot-name">Behind the Facade</strong>'
        '<p>Melbourne construction. The conversations behind the work.</p>'
        '<div class="foot-links"><a href="' + SHOW['spotify'] + '">Spotify</a><a href="' + SHOW['apple'] + '">Apple</a>'
        '<a href="' + SHOW['youtube'] + '">YouTube</a><a href="/feed">RSS</a>'
        '<a href="mailto:contact@thebtfpodcast.com">contact@thebtfpodcast.com</a></div></div>'
        '<form class="subscribe" name="subscribe" method="POST" data-netlify="true" netlify-honeypot="bot-field">'
        '<input type="hidden" name="form-name" value="subscribe">'
        '<p class="hide"><label>Do not fill this out <input name="bot-field"></label></p>'
        '<label>Subscribe<span class="sub-row">'
        '<input type="email" name="email" required placeholder="Email address">'
        '<button class="btn" type="submit">Join</button></span></label>'
        '<p class="sub-note">Episodes and notes. No noise.</p></form></div></footer></body></html>'
    )

def render_home(latest, rest, hosts, guests, count):
    bg = html.escape(latest['image'])
    yt = SHOW['youtube']
    guest_cards = ''
    for g in guests[:3]:
        guest_cards += (
            '<a class="card" href="/guests/"><img src="/thumbs/' + g['episode'] + '.jpg" alt="">'
            '<div class="body"><p class="meta">Episode ' + html.escape(g['episode']) + '</p>'
            '<h3>' + html.escape(g['name']) + '</h3><p>' + html.escape(g['summary']) + '</p></div></a>'
        )
    pillars = (
        '<a class="pillar" href="/episodes/' + latest['slug'] + '/">'
        '<img src="' + bg + '" alt="">'
        '<div class="body"><p class="meta">Now playing</p><h3>' + html.escape(latest['title']) + '</h3>'
        '<p>' + html.escape(latest['excerpt']) + '</p></div></a>'
        '<a class="pillar" href="/hosts/">'
        '<img src="/cover.jpg" alt="">'
        '<div class="body"><p class="meta">The hosts</p><h3>Jake and Daniel</h3>'
        '<p>Proline and Complex Facade. Two contractors, one fortnightly conversation.</p></div></a>'
        '<a class="pillar" href="/articles/">'
        '<img src="/hero.jpg" alt="">'
        '<div class="body"><p class="meta">Field notes</p><h3>Quiet reading on the work</h3>'
        '<p>Pipeline, labour, packages and the numbers behind the week.</p></div></a>'
    )
    return (
        '<main>'
        '<section class="stage"><div class="stage-bg" style="background-image:url(/hero.jpg),url(' + FALLBACK + ')"></div>'
        '<div class="stage-shade"></div><div class="wrap stage-copy">'
        '<p class="kicker">Melbourne construction podcast</p>'
        '<h1>The conversations<br>behind the work.</h1>'
        '<p class="lede">' + html.escape(SHOW['tagline']) + '</p>'
        '<div class="btns">'
        '<a class="btn" href="/episodes/' + latest['slug'] + '/">Watch the latest</a>'
        '<a class="text-link" href="' + yt + '" target="_blank" rel="noreferrer">YouTube</a>'
        '</div></div></section>'
        '<section class="wrap intro">'
        '<p class="kicker">The show</p>'
        '<h2>One intelligent conversation.<br>The unfiltered version.</h2>'
        '<div class="pillars">' + pillars + '</div>'
        '</section>'
        '<section class="wrap">'
        '<div class="section-head"><h2>Archive</h2><a href="/episodes/">All episodes</a></div>'
        '<div class="grid">' + ''.join(
            '<a class="card" href="/episodes/' + e['slug'] + '/"><img src="' + html.escape(e['image']) + '" alt="">'
            '<div class="body"><p class="meta">Ep ' + html.escape(e['episode']) + ' · ' + html.escape(e['duration']) + '</p>'
            '<h3>' + html.escape(e['title']) + '</h3></div></a>' for e in rest
        ) + '</div></section>'
        '<section class="wrap">'
        '<div class="section-head"><h2>Hosts</h2><a href="/hosts/">Full bios</a></div>'
        '<div class="split">'
        '<div class="host"><p class="kicker">Host</p><h3>Jake Gorry</h3><p>' + html.escape(hosts[0]['summary']) + '</p><a class="text-link" href="/hosts/">Read Jake</a></div>'
        '<div class="host"><p class="kicker">Host</p><h3>Daniel Alizzi</h3><p>' + html.escape(hosts[1]['summary']) + '</p><a class="text-link" href="/hosts/">Read Daniel</a></div>'
        '</div></section>'
        '<section class="wrap last">'
        '<div class="section-head"><h2>Guests</h2><a href="/guests/">All guests</a></div>'
        '<div class="grid">' + guest_cards + '</div>'
        '</section></main>'
    )
