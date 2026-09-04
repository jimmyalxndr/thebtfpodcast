import base64
from pathlib import Path

def write_hero(dest):
    parts=[]
    from hero_0 import P as p0
    parts.append(p0)
    from hero_1 import P as p1
    parts.append(p1)
    from hero_2 import P as p2
    parts.append(p2)
    from hero_3 import P as p3
    parts.append(p3)
    from hero_4 import P as p4
    parts.append(p4)
    from hero_5 import P as p5
    parts.append(p5)
    Path(dest).write_bytes(base64.b64decode(''.join(parts)))
