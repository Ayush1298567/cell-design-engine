"""Fetch the Chen2020 LG M50 validation dataset (Zenodo 4032561).

The raw CSVs are not committed (they have a canonical home and the repo stays
lean). Run this once to populate data/, with MD5 verification so a corrupted or
changed download is caught. CC BY 4.0; see data/README.md for attribution.
"""

import hashlib
import os
import urllib.request

BASE = "https://zenodo.org/records/4032561/files"
FILES = {
    "LGM50_cell02.csv": "0bbf959cbfc367296ec69d7a74d2f5c1",
    "LGM50_cell03.csv": "a09cbd8eff0af55dfe9bc8728fa89908",
    "LGM50_cell04.csv": "f17615476283d2e15087165697ff9d7c",
}
HERE = os.path.dirname(os.path.abspath(__file__))


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


for name, expected in FILES.items():
    dest = os.path.join(HERE, name)
    if os.path.exists(dest) and md5(dest) == expected:
        print(f"ok (cached):  {name}")
        continue
    print(f"downloading:  {name}")
    urllib.request.urlretrieve(f"{BASE}/{name}?download=1", dest)
    got = md5(dest)
    if got != expected:
        raise SystemExit(f"MD5 mismatch for {name}: expected {expected}, got {got}")
    print(f"ok:           {name}")

print("all files present and verified")
