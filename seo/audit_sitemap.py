import glob
import io
import os
import re
import xml.etree.ElementTree as ET

# 1. XML validity
raw = io.open("sitemap.xml", encoding="utf-8", newline="").read()
try:
    ET.fromstring(raw)
    print("XML: valid")
except Exception as e:
    print(f"XML: INVALID - {e}")

locs = re.findall(r"<loc>(.*?)</loc>", raw)
print(f"Total URLs: {len(locs)}")

# 2. Duplicates
dupes = {u for u in locs if locs.count(u) > 1}
print("Duplicates:", dupes if dupes else "none")

# 3. Every sitemap URL maps to a real file
missing = []
for u in locs:
    path = u.replace("https://securelocksmithsolution.com/", "")
    path = "index.html" if path == "" else path
    if not os.path.exists(path):
        missing.append(u)
print("URLs with no matching file:", missing if missing else "none")

# 4. Entries that should NOT be in a sitemap
for u in locs:
    if "serv_form.html" in u or "thank_you" in u or "/images/" in u:
        print("SHOULD NOT BE LISTED:", u)

# 5. Real pages missing from the sitemap
listed = {u.replace("https://securelocksmithsolution.com/", "") or "index.html" for u in locs}
skip = {"serv_form.html", "thank_you.html"}  # redirect stub / thank-you page
not_listed = [p for p in sorted(glob.glob("*.html")) if p not in listed and p not in skip]
print("Live pages NOT in sitemap:", not_listed if not_listed else "none")

# 6. robots.txt disallowed paths must not be listed
robots = io.open("robots.txt", encoding="utf-8").read()
disallowed = re.findall(r"Disallow: (\S+)", robots)
for u in locs:
    for d in disallowed:
        if d != "/" and d.lstrip("/") in u:
            print("CONFLICT with robots.txt:", u)
print("robots.txt conflicts: check complete")
