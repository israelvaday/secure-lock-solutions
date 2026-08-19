import urllib.request

req = urllib.request.Request(
    "https://securelocksmithsolution.com/?v=footer1",
    headers={"Cache-Control": "no-cache"},
)
h = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
print("footer-grid present:", "footer-grid" in h)
print("fontawesome linked:", "fontawesome-all.min.css" in h)
print("copyright present:", "© 2026 Secure Lock Solutions" in h or "&copy; 2026" in h)
