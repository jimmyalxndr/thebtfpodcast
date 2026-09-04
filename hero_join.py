import base64
from pathlib import Path
from hero_b64 import B64

def write_hero(dest):
    Path(dest).write_bytes(base64.b64decode(B64))
