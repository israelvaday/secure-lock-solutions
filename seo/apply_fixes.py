"""Apply Semrush audit fixes across static HTML site."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TITLE_MAP = {
    "index.html": "Orange County Locksmith | 24/7 Emergency | Secure Lock Solutions",
    "smart-locks.html": "Smart Lock Installation | Keyless Entry | Secure Lock Solutions",
    "blog004.html": "10 Home Security Tips | Orange County | Secure Lock Solutions",
    "blog003.html": "Locked Out? Emergency Guide | Secure Lock Solutions",
}

CITY_TITLE_RE = re.compile(
    r"Locksmith in (.+?) CA \| 24/7 Emergency Service \| Secure Lock Solutions"
)

FOOTER_LINKS = """                        <div id="copyright">
                            <ul class="menu">
                                <li><a href="service-areas.html">Service Areas</a></li>
                                <li><a href="hours.html">Hours</a></li>
                                <li><a href="blog.html">Blog</a></li>
                                <li><a href="emergency.html">Emergency</a></li>
                                <li><a href="serv-form.html">Book Service</a></li>
                            </ul>
                            <ul class="menu">"""

NAV_EXTRA = """                                    <li><a href="blog.html">Blog</a></li>
                                    <li><a href="hours.html">Hours</a></li>"""

REDIRECT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Redirecting to booking form</title>
  <link rel="canonical" href="https://securelocksmithsolution.com/serv-form.html">
  <meta http-equiv="refresh" content="0;url=serv-form.html">
  <script>location.replace("serv-form.html");</script>
</head>
<body><p><a href="serv-form.html">Continue to booking form</a></p></body>
</html>"""


def migrate_booking_form() -> None:
    src = ROOT / "serv_form.html"
    dst = ROOT / "serv-form.html"
    text = src.read_text(encoding="utf-8")
    text = text.replace("serv_form.html", "serv-form.html")
    text = text.replace(
        "https://securelocksmithsolution.com/serv_form.html",
        "https://securelocksmithsolution.com/serv-form.html",
    )
    if "<h1>" not in text:
        text = text.replace(
            '<h2><i class="fas fa-calendar-check"></i> Book Your Appointment</h2>',
            '<h1><i class="fas fa-calendar-check"></i> Request Locksmith Service</h1>\n    '
            '<h2><i class="fas fa-calendar-check"></i> Book Your Appointment</h2>',
        )
    dst.write_text(text, encoding="utf-8")
    src.write_text(REDIRECT, encoding="utf-8")
    print("migrated serv-form.html")


def replace_links() -> None:
    for path in ROOT.glob("*.html"):
        if path.name == "serv_form.html":
            continue
        content = path.read_text(encoding="utf-8")
        updated = content.replace("serv_form.html", "serv-form.html")
        if updated != content:
            path.write_text(updated, encoding="utf-8")
            print("links", path.name)


def shorten_titles() -> None:
    for path in ROOT.glob("*.html"):
        content = path.read_text(encoding="utf-8")
        if path.name in TITLE_MAP:
            new_title = TITLE_MAP[path.name]
        else:
            match = CITY_TITLE_RE.search(content)
            if not match:
                continue
            new_title = f"{match.group(1)} Locksmith | 24/7 | Secure Lock Solutions"
        updated = content
        updated = re.sub(r"<title>[^<]+</title>", f"<title>{new_title}</title>", updated, count=1)
        updated = re.sub(
            r'<meta property="og:title" content="[^"]+"',
            f'<meta property="og:title" content="{new_title}"',
            updated,
            count=1,
        )
        updated = re.sub(
            r'"name": "Locksmith in [^"]+"',
            f'"name": "{new_title}"',
            updated,
            count=1,
        )
        if updated != content:
            path.write_text(updated, encoding="utf-8")
            print("title", path.name, len(new_title))


def fix_learn_more() -> None:
    fixes = {
        "index.html": ">Licensed & insured locksmith</a>",
        "residential.html": ">Licensed residential locksmith</a>",
        "commercial.html": ">Licensed commercial locksmith</a>",
        "service-areas.html": ">Licensed Orange County locksmith</a>",
    }
    for name, replacement in fixes.items():
        path = ROOT / name
        content = path.read_text(encoding="utf-8")
        marker = "licensed-insured.html"
        idx = content.find(marker)
        if idx == -1:
            continue
        segment = content[idx:]
        if ">Learn More</a>" in segment:
            segment = segment.replace(">Learn More</a>", replacement, 1)
        elif ">Learn more</a>" in segment:
            segment = segment.replace(">Learn more</a>", replacement, 1)
        else:
            continue
        path.write_text(content[:idx] + segment, encoding="utf-8")
        print("anchor", name)


def add_footer_and_nav() -> None:
    for path in ROOT.glob("*.html"):
        if path.name == "serv_form.html":
            continue
        content = path.read_text(encoding="utf-8")
        original = content
        if "Book Service</a></li>" not in content and '<div id="copyright">' in content:
            content = content.replace('<div id="copyright">', FOOTER_LINKS, 1)
        if (
            'href="blog.html">Blog</a>' not in content
            and 'id="nav"' in content
            and 'service-areas.html">Service Areas</a></li>' in content
        ):
            content = content.replace(
                'service-areas.html">Service Areas</a></li>',
                'service-areas.html">Service Areas</a></li>\n' + NAV_EXTRA,
                1,
            )
        if content != original:
            path.write_text(content, encoding="utf-8")
            print("footer/nav", path.name)


def update_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    content = path.read_text(encoding="utf-8").replace("serv_form.html", "serv-form.html")
    path.write_text(content, encoding="utf-8")
    print("sitemap updated")


def main() -> None:
    migrate_booking_form()
    replace_links()
    shorten_titles()
    fix_learn_more()
    add_footer_and_nav()
    update_sitemap()


if __name__ == "__main__":
    main()
