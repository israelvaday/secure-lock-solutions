"""Self-host AOS: swap broken cdnjs URLs (404) for local files and guard init."""
import glob
import io
import re

CSS_CDN = re.compile(r'https://cdnjs\.cloudflare\.com/ajax/libs/aos/2\.3\.4/aos(\.min)?\.css')
JS_CDN = re.compile(r'https://cdnjs\.cloudflare\.com/ajax/libs/aos/2\.3\.4/aos(\.min)?\.js')
INIT = re.compile(r'(?<!window\.AOS && )\bAOS\.init\(')

changed = 0
for path in sorted(glob.glob("*.html")):
    html = io.open(path, encoding="utf-8", newline="").read()
    orig = html
    html = CSS_CDN.sub("assets/css/aos.min.css", html)
    html = JS_CDN.sub("assets/js/aos.min.js", html)
    html = INIT.sub("window.AOS && AOS.init(", html)
    if html != orig:
        io.open(path, "w", encoding="utf-8", newline="").write(html)
        changed += 1

print(f"updated {changed} files")

# verify nothing left pointing at the CDN
left = [p for p in glob.glob("*.html")
        if "cdnjs.cloudflare.com/ajax/libs/aos" in io.open(p, encoding="utf-8", newline="").read()]
print("remaining CDN refs:", left or "none")
