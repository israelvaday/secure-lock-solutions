import re
import urllib.request

h = urllib.request.urlopen(
    "https://securelocksmithsolution.com/sitemap.xml", timeout=30
).read().decode("utf-8")
locs = re.findall(r"<loc>(.*?)</loc>", h)
print("Live sitemap URLs:", len(locs))
print("rancho-santa-margarita present:", any("rancho-santa-margarita" in u for u in locs))
print("lastmod sample:", re.findall(r"<lastmod>(.*?)</lastmod>", h)[:3])
