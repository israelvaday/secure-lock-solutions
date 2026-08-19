import re
import urllib.request

for url in [
    "https://securelocksmithsolution.com/",
    "https://securelocksmithsolution.com/anaheim.html",
    "https://securelocksmithsolution.com/emergency.html",
]:
    h = urllib.request.urlopen(url, timeout=30).read().decode("utf-8")
    t = re.search(r"<title>(.*?)</title>", h).group(1)
    d = re.search(r'name="description" content="(.*?)"', h, re.DOTALL).group(1)
    print(url)
    print("  T:", t)
    print("  D:", d[:140])
    print("  has 24/7:", "24/7" in h)
