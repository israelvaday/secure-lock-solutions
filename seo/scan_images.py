"""Find every raster image actually referenced by pages and CSS."""
import glob
import io
import re
from collections import Counter

refs = Counter()
where = {}

patterns = [
    re.compile(r'(?:src|href)="(images/[^"]+?\.(?:png|jpe?g))"', re.IGNORECASE),
    re.compile(r'url\("?(images/[^")]+?\.(?:png|jpe?g))"?\)', re.IGNORECASE),
    re.compile(r'content="(https://securelocksmithsolution\.com/)?(images/[^"]+?\.(?:png|jpe?g))"', re.IGNORECASE),
]

files = sorted(glob.glob("*.html")) + sorted(glob.glob("assets/css/*.css"))
for path in files:
    text = io.open(path, encoding="utf-8", newline="").read()
    for pat in patterns:
        for m in re.finditer(pat, text):
            img = m.group(m.lastindex)  # last group = image path
            refs[img] += 1
            where.setdefault(img, set()).add(path)

print(f"Referenced raster images: {len(refs)}\n")
for img, count in refs.most_common():
    print(f"{img}  ({count} refs)")
