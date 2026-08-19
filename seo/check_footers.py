import glob
import io
import re

footers = {}
for p in sorted(glob.glob("*.html")):
    h = io.open(p, encoding="utf-8", newline="").read()
    m = re.search(r'<footer[^>]*id="footer".*?</footer>', h, re.DOTALL)
    if not m:
        m = re.search(r"<footer.*?</footer>", h, re.DOTALL)
    if m:
        text = re.sub(r"<[^>]+>", " ", m.group(0))
        text = re.sub(r"\s+", " ", text).strip()
        footers[p] = text
    else:
        footers[p] = None

no_footer = [p for p, t in footers.items() if t is None]
print("Pages with NO footer:", no_footer if no_footer else "none")

# Group identical footers to spot inconsistencies
groups = {}
for p, t in footers.items():
    if t:
        groups.setdefault(t, []).append(p)

print(f"\nDistinct footer versions: {len(groups)}")
for i, (text, pages) in enumerate(groups.items(), 1):
    print(f"\n--- Footer variant {i} ({len(pages)} pages, e.g. {pages[0]}) ---")
    print(text[:600])
