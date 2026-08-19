import glob
import io
import os
import re

broken = 0
for p in sorted(glob.glob("*.html")):
    html = io.open(p, encoding="utf-8").read()
    for m in re.finditer(r'(?:href|src)="([^"#]+?)(?:#[^"]*)?"', html):
        url = m.group(1)
        if re.match(r"^(https?:|mailto:|tel:|data:|javascript:)", url):
            continue
        target = url.split("?")[0]
        if target and not os.path.exists(target):
            broken += 1
            print(f"BROKEN {p}: {url}")
print("All internal links OK" if broken == 0 else f"{broken} broken links")
