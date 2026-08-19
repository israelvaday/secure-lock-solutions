import re
import urllib.request

for url in [
    "https://securelocksmithsolution.com/aliso-viejo.html",
    "https://securelocksmithsolution.com/emergency.html",
    "https://securelocksmithsolution.com/automotive.html",
]:
    h = urllib.request.urlopen(url, timeout=30).read().decode("utf-8")
    bad = re.findall(
        r"24/7|24 Hours / 7 Days|24 hours a day|7 days a week|around the clock|365 days",
        h,
        re.IGNORECASE,
    )
    footer_hours = re.search(r"<dt>Hours</dt>\s*<dd>(.*?)</dd>", h, re.DOTALL)
    print(url)
    print("  inaccurate claims:", bad if bad else "none")
    if footer_hours:
        print("  footer hours:", re.sub(r"<[^>]+>", " ", footer_hours.group(1)).strip())
