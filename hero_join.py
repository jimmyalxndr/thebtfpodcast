import base64
from pathlib import Path

def write_hero(dest):
    from hero_0 import P as p0
    from hero_1 import P as p1
    from hero_2 import P as p2
    from hero_3 import P as p3
    from hero_4 import P as p4
    from hero_5 import P as p5
    from hero_6 import P as p6
    from hero_7 import P as p7
    Path(dest).write_bytes(base64.b64decode(p0 + p1 + p2 + p3 + p4 + p5 + p6 + p7))
