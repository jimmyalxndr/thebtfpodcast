#!/usr/bin/env python3
from __future__ import annotations
import html, re, shutil, urllib.parse, urllib.request
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET
from site_config import RSS_URL, COVER_URL, SITE, ITUNES, SHOW

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
CSS = (ROOT / "styles.css").read_text(encoding="utf-8")

def slugify(title, episode):
    cleaned = re.sub(r"[^a-z0-9]+", "-", re.sub(r"^#?\d+\s*-\s*", "", title.lower())).strip("-")[:80]
    return f"{episode}-{cleaned}" if episode else cleaned

def plain(raw):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw or ""))).strip()

def excerpt(text, n=180):
    return text if len(text) <= n else text[:n].rsplit(" ", 1)[0] + "…"

def duration(seconds):
    try:
        s = int(float(seconds))
    except Exception:
        return ""
    h, m = divmod(s, 3600)
    m, _ = divmod(m, 60)
    return f"{h}h {m:02d}m" if h else f"{m} min"

def date_label(rfc):
    try:
        return datetime.strptime((rfc or "")[:25], "%a, %d %b %Y %H:%M:%S").strftime("%d %b %Y")
    except Exception:
        return rfc or ""

def fetch():
    req = urllib.request.Request(RSS_URL, headers={"User-Agent": "thebtfpodcast-site/1.0"})
    with urllib.request.urlopen(req, timeout=30) as res:
        root = ET.fromstring(res.read())
    out = []
    for item in root.find("channel").findall("item"):
        title = (item.findtext("title") or "Untitled").strip()
        ep = (item.findtext(f"{ITUNES}episode") or "").strip()
        desc = item.findtext("description") or ""
        enc = item.find("enclosure")
        img = item.find(f"{ITUNES}image")
        out.append({
            "title": title, "episode": ep, "slug": slugify(title, ep),
            "dateLabel": date_label(item.findtext("pubDate")),
            "duration": duration(item.findtext(f"{ITUNES}duration") or "0"),
            "audioUrl": enc.get("url") if enc is not None else "",
            "image": img.get("href") if img is not None else "/cover.jpg",
            "descriptionHtml": desc, "excerpt": excerpt(plain(desc)),
        })
    return out

def layout(title, path, description, body, image="/cover.jpg"):
    abs_img = image if image.startswith("http") else SITE + image
    page = title if title == SHOW["title"] else f"{title} \u00b7 {SHOW['title']}"
    return (
        "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        f"<title>{html.escape(page)}</title>"
        f"<meta name=\"description\" content=\"{html.escape(description)}\">"
        f"<link rel=\"canonical\" href=\"{SITE + path}\"><link rel=\"icon\" href=\"/cover.jpg\">"
        "<link href=\"https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&display=swap\" rel=\"stylesheet\">"
        f"<meta property=\"og:title\" content=\"{html.escape(title)}\">"
        f"<meta property=\"og:image\" content=\"{html.escape(abs_img)}\">"
        "<link rel=\"stylesheet\" href=\"/styles.css\"></head><body>"
        f"<header><div class=\"wrap nav\"><a class=\"brand\" href=\"/\"><img src=\"/cover.jpg\" alt=\"\">Behind the Facade</a>"
        f"<nav><a href=\"/episodes/\">Episodes</a><a href=\"/about/\">About</a><a href=\"/guests/\">Be a guest</a>"
        f"<a href=\"{SHOW['youtube']}\" target=\"_blank\" rel=\"noreferrer\">YouTube</a></nav></div></header>"
        f"{body}<footer><div class=\"wrap foot\"><div><strong style=\"color:#fff\">Behind the Facade</strong>"
        "<div>Melbourne construction podcast \u00b7 Jake Gorry & Daniel Alizzi</div></div>"
        f"<div><a href=\"{SHOW['spotify']}\">Spotify</a><a href=\"{SHOW['apple']}\">Apple</a>"
        f"<a href=\"{SHOW['youtube']}\">YouTube</a><a href=\"/feed\">RSS</a></div></div></footer></body></html>"
    )

def buttons(compact=False):
    extra = "" if compact else f"<a class=\"btn ghost\" href=\"{SHOW['rss']}\" target=\"_blank\" rel=\"noreferrer\">RSS</a>"
    return (
        f"<div class=\"btns\"><a class=\"btn\" href=\"{SHOW['youtube']}\" target=\"_blank\" rel=\"noreferrer\">YouTube</a>"
        f"<a class=\"btn ghost\" href=\"{SHOW['spotify']}\" target=\"_blank\" rel=\"noreferrer\">Spotify</a>"
        f"<a class=\"btn ghost\" href=\"{SHOW['apple']}\" target=\"_blank\" rel=\"noreferrer\">Apple</a>{extra}</div>"
    )

def put(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding=\"utf-8\")

def card(ep):
    return (
        f"<a class=\"card\" href=\"/episodes/{ep['slug']}/\"><img src=\"{html.escape(ep['image'])}\" alt=\"\">"
        f"<div class=\"body\"><p class=\"meta\">Ep {html.escape(ep['episode'])} \u00b7 {html.escape(ep['duration'])}</p>"
        f"<h3>{html.escape(ep['title'])}</h3></div></a>"
    )

def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    req = urllib.request.Request(COVER_URL, headers={"User-Agent": "thebtfpodcast-site/1.0"})
    with urllib.request.urlopen(req, timeout=30) as res:
        (DIST / "cover.jpg").write_bytes(res.read())
    (DIST / "styles.css").write_text(CSS, encoding="utf-8")
    episodes = fetch()
    latest, rest = episodes[0], episodes[1:7]
    home = (
        f"<main><section class=\"wrap hero\"><img class=\"hero-art\" src=\"/cover.jpg\" alt=\"\">"
        f"<div><p class=\"kicker\">Construction podcast \u00b7 Melbourne \u00b7 @BehindTheFacadeShow</p>"
        f"<h1>Behind<br>the Facade</h1><p class=\"lede\">{SHOW['tagline']}</p>{buttons()}</div></section>"
        f"<section class=\"wrap\"><div class=\"section-head\"><h2>Latest episode</h2><a href=\"/episodes/\">All episodes</a></div>"
        f"<article class=\"latest\"><img src=\"{html.escape(latest['image'])}\" alt=\"\"><div>"
        f"<p class=\"meta\">Episode {html.escape(latest['episode'])} \u00b7 {html.escape(latest['dateLabel'])} \u00b7 {html.escape(latest['duration'])}</p>"
        f"<h3><a href=\"/episodes/{latest['slug']}/\">{html.escape(latest['title'])}</a></h3>"
        f"<p>{html.escape(latest['excerpt'])}</p><div class=\"btns\"><a class=\"btn\" href=\"/episodes/{latest['slug']}/\">Play episode</a>"
        f"<a class=\"btn ghost\" href=\"{SHOW['youtube']}\" target=\"_blank\" rel=\"noreferrer\">Watch on YouTube</a></div>"
        f"</div></article></section><section class=\"wrap\"><div class=\"section-head\"><h2>Recent</h2></div>"
        f"<div class=\"grid\">{''.join(card(e) for e in rest)}</div></section>"
        f"<section class=\"wrap\"><div class=\"section-head\"><h2>The hosts</h2><a href=\"/about/\">More</a></div>"
        f"<div class=\"split\"><div class=\"host\"><p class=\"kicker\">Host</p><h3>Jake Gorry</h3>"
        f"<p>Director of Proline Group. Started on the tools at 14.</p>"
        f"<a class=\"btn ghost\" href=\"{SHOW['jake']}\" target=\"_blank\" rel=\"noreferrer\">LinkedIn</a></div>"
        f"<div class=\"host\"><p class=\"kicker\">Host</p><h3>Daniel Alizzi</h3>"
        f"<p>Operations Manager at Complex Facade Install.</p>"
        f"<a class=\"btn ghost\" href=\"{SHOW['daniel']}\" target=\"_blank\" rel=\"noreferrer\">LinkedIn</a></div></div></section></main>"
    )
    put(DIST / "index.html", layout(SHOW["title"], "/", SHOW["description"], home))
    archive = (
        "<main class=\"wrap\"><div class=\"page-hero\"><p class=\"kicker\">Archive</p><h1>Episodes</h1></div>"
        f"<div class=\"grid\" style=\"padding-bottom:64px\">{''.join(card(e) for e in episodes)}</div></main>"
    )
    put(DIST / "episodes/index.html", layout("Episodes", "/episodes/", "Every episode of Behind the Facade.", archive))
    for ep in episodes:
        watch = "https://www.youtube.com/@BehindTheFacadeShow/search?query=" + urllib.parse.quote(ep["title"])
        audio = f"<audio controls preload=\"none\" src=\"{html.escape(ep['audioUrl'])}\"></audio>" if ep["audioUrl"] else ""
        body = (
            f"<main class=\"wrap\"><div class=\"page-hero\"><p class=\"kicker\">Episode {html.escape(ep['episode'])} \u00b7 {html.escape(ep['dateLabel'])} \u00b7 {html.escape(ep['duration'])}</p>"
            f"<h1 style=\"font-size:clamp(28px,4vw,48px);text-transform:none\">{html.escape(ep['title'])}</h1></div>"
            f"<article class=\"ep\"><aside><img src=\"{html.escape(ep['image'])}\" alt=\"\">{buttons(True)}</aside>"
            f"<div>{audio}<p><a class=\"btn ghost\" href=\"{watch}\" target=\"_blank\" rel=\"noreferrer\">Find this episode on YouTube</a></p>"
            f"<div class=\"notes\">{ep['descriptionHtml']}</div></div></article></main>"
        )
        put(DIST / "episodes" / ep["slug"] / "index.html", layout(ep["title"], f"/episodes/{ep['slug']}/", ep["excerpt"], body, ep["image"]))
    about = (
        f"<main class=\"wrap\" style=\"padding-bottom:72px\"><div class=\"page-hero\"><p class=\"kicker\">The show</p><h1>About</h1>"
        f"<p class=\"lede\">{html.escape(SHOW['description'])}</p></div>"
        f"<div class=\"split\"><div class=\"host\"><p class=\"kicker\">Host</p><h3>Jake Gorry</h3>"
        f"<p>Founder and director of Proline Group.</p>"
        f"<a class=\"btn ghost\" href=\"{SHOW['jake']}\" target=\"_blank\" rel=\"noreferrer\">LinkedIn</a></div>"
        f"<div class=\"host\"><p class=\"kicker\">Host</p><h3>Daniel Alizzi</h3>"
        f"<p>Operations Manager at Complex Facade Install Pty Ltd.</p>"
        f"<a class=\"btn ghost\" href=\"{SHOW['daniel']}\" target=\"_blank\" rel=\"noreferrer\">LinkedIn</a></div></div></main>"
    )
    put(DIST / "about/index.html", layout("About", "/about/", SHOW["description"], about))
    guests = (
        "<main class=\"wrap\" style=\"padding-bottom:72px\"><div class=\"page-hero\"><p class=\"kicker\">Bookings</p><h1>Be a guest</h1>"
        "<p class=\"lede\">Pitch a guest or a topic for the show.</p></div>"
        "<form name=\"guest\" method=\"POST\" data-netlify=\"true\" netlify-honeypot=\"bot-field\">"
        "<input type=\"hidden\" name=\"form-name\" value=\"guest\">"
        "<p style=\"display:none\"><label>Don’t fill this out <input name=\"bot-field\"></label></p>"
        "<label>Name <input type=\"text\" name=\"name\" required></label>"
        "<label>Email <input type=\"email\" name=\"email\" required></label>"
        "<label>Company / role <input type=\"text\" name=\"company\"></label>"
        "<label>Why this conversation <textarea name=\"pitch\" required></textarea></label>"
        "<button class=\"btn\" type=\"submit\">Send pitch</button></form></main>"
    )
    put(DIST / "guests/index.html", layout("Be a guest", "/guests/", "Pitch a guest for Behind the Facade.", guests))
    print(f"Built {len(episodes)} episodes")

if __name__ == \"__main__\":
    build()
