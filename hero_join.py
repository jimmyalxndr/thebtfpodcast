import base64
from pathlib import Path

def write_hero(dest):
    from hero_0 import P as a
    from hero_1 import P as b
    from hero_2 import P as c
    from hero_3 import P as d
    Path(dest).write_bytes(base64.b64decode(a + b + c + d))
