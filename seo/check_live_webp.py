"""Verify live site serves WebP images after deploy."""
import urllib.request

BASE = "https://securelocksmithsolution.com/"

html = urllib.request.urlopen(BASE + "?v=webp1", timeout=30).read().decode("utf-8", "ignore")
uses_webp = "images/header-hero.webp" in html
og_jpg = "images/header-hero.jpg" in html
print(f"homepage references hero .webp: {uses_webp}")
print(f"og:image still .jpg: {og_jpg}")

req = urllib.request.Request(BASE + "images/header-hero.webp")
r = urllib.request.urlopen(req, timeout=30)
data = r.read()
print(f"hero webp: HTTP {r.status}, {r.headers.get('Content-Type')}, {len(data)/1024:.0f} KB")

req = urllib.request.Request(BASE + "images/header-hero.jpg")
r = urllib.request.urlopen(req, timeout=30)
print(f"hero jpg (og:image fallback): HTTP {r.status}, {len(r.read())/1024:.0f} KB")
