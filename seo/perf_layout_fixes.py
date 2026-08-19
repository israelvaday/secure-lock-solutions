"""Performance + layout fixes:
1. Convert truck-hero.png (2.8 MB, hero on every page) to WebP; update main.css.
2. Global overflow-x guard so AOS slide animations can't widen the page.
3. Fix index.html preload: point at the real hero with the right MIME type.
4. Add loading="lazy" + decoding="async" to content images (skips logos/favicons
   and images that already declare a loading attribute).
"""
import glob
import io
import os
import re

from PIL import Image

# 1. hero conversion
src = "images/truck-hero.png"
dst = "images/truck-hero.webp"
img = Image.open(src).convert("RGB")
img.save(dst, "WEBP", quality=82, method=6)
print(f"hero: {os.path.getsize(src)//1024} KB png -> {os.path.getsize(dst)//1024} KB webp")

css = io.open("assets/css/main.css", encoding="utf-8", newline="").read()
css = css.replace('url("../../images/truck-hero.png")', 'url("../../images/truck-hero.webp")')

# 2. global overflow guard (existing rule only applies under 980px)
GUARD = "\n/* Prevent AOS slide animations from widening the page */\nhtml, body {\n\toverflow-x: hidden;\n}\n"
if "Prevent AOS slide animations" not in css:
    css += GUARD
io.open("assets/css/main.css", "w", encoding="utf-8", newline="").write(css)
print("main.css updated")

# 3. preload fix on index.html
html = io.open("index.html", encoding="utf-8", newline="").read()
html = html.replace(
    '<link rel="preload" href="images/header-hero.webp" as="image" type="image/jpeg">',
    '<link rel="preload" href="images/truck-hero.webp" as="image" type="image/webp">',
)
io.open("index.html", "w", encoding="utf-8", newline="").write(html)
print("index.html preload fixed")

# 4. lazy-load content images
IMG_TAG = re.compile(r"<img\b[^>]*>", re.IGNORECASE)

def add_lazy(tag: str) -> str:
    if "loading=" in tag or "logo" in tag.lower() or "favicon" in tag.lower():
        return tag
    insert = ' loading="lazy" decoding="async"'
    if tag.endswith("/>"):
        return tag[:-2].rstrip() + insert + " />"
    return tag[:-1] + insert + ">"

changed = 0
total_tagged = 0
for path in sorted(glob.glob("*.html")):
    text = io.open(path, encoding="utf-8", newline="").read()
    new_text, n = IMG_TAG.subn(lambda m: add_lazy(m.group(0)), text)
    if new_text != text:
        io.open(path, "w", encoding="utf-8", newline="").write(new_text)
        changed += 1
        total_tagged += sum(1 for m in IMG_TAG.finditer(new_text) if 'loading="lazy"' in m.group(0))
print(f"lazy-loading applied in {changed} files")
