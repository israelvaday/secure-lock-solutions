import glob
import io
import json
import re

bad = 0
for p in sorted(glob.glob("*.html")):
    html = io.open(p, encoding="utf-8").read()
    for i, m in enumerate(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)):
        try:
            json.loads(m.group(1))
        except Exception as e:
            bad += 1
            print(f"INVALID {p} block {i}: {e}")
print("All JSON-LD valid" if bad == 0 else f"{bad} invalid blocks")
