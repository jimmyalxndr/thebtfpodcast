import urllib.request
from pathlib import Path

HERO_URL = 'https://i.imgur.com/6VoEV7C.jpeg'

def write_hero(dest):
    req = urllib.request.Request(HERO_URL, headers={'User-Agent': 'thebtfpodcast-site/1.0'})
    with urllib.request.urlopen(req, timeout=30) as res:
        data = res.read()
    if data[:3] != b'\xff\xd8':
        raise RuntimeError('hero download was not a JPEG')
    Path(dest).write_bytes(data)
