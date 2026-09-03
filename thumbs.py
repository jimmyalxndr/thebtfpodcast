import urllib.request
from pathlib import Path

def grab(url, dest):
    req = urllib.request.Request(url, headers={'User-Agent': 'thebtfpodcast-site/1.0'})
    with urllib.request.urlopen(req, timeout=20) as res:
        dest.write_bytes(res.read())

def pull_thumb(vid, dest):
    for name in ('maxresdefault.jpg', 'sddefault.jpg', 'hqdefault.jpg'):
        try:
            grab('https://i.ytimg.com/vi/' + vid + '/' + name, dest)
            return True
        except Exception:
            continue
    return False
