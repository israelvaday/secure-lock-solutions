import glob
import io
import re

PATTERNS = [
    r"24/7",
    r'href="Emergency',
    r" \.</",
    r" ,",
    r"\bEmergency Emergency\b",
    r"\| \|",
    r"available\. Emergency service available",
    r"available 24",
]

bad = 0
for p in sorted(glob.glob("*.html")):
    h = io.open(p, encoding="utf-8", newline="").read()
    for pat in PATTERNS:
        for m in re.finditer(pat, h):
            bad += 1
            s = max(0, m.start() - 50)
            snippet = h[s : m.end() + 50].replace("\n", " ").replace("\r", "")
            print(p, "::", pat, "::", snippet)
print("CLEAN" if bad == 0 else f"{bad} issues")
