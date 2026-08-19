"""Link the local Font Awesome stylesheet on every page that uses FA icons
but doesn't load any Font Awesome CSS. Preserves line endings."""
import glob
import io
import re
import sys

FA_LINK = '<link rel="stylesheet" href="assets/css/fontawesome-all.min.css" />'
MAIN_CSS_LINK = re.compile(r'(<link rel="stylesheet" href="assets/css/main\.css"\s*/?>)')


def main() -> None:
    changed, skipped = [], []
    for path in sorted(glob.glob("*.html")):
        with io.open(path, "r", encoding="utf-8", newline="") as f:
            html = f.read()

        uses_icons = re.search(r'class="[^"]*\b(fa[sb]?|fab|fas|far)\s+fa-', html)
        has_fa_css = "fontawesome" in html.lower() or "font-awesome" in html.lower()

        if not uses_icons or has_fa_css:
            skipped.append(path)
            continue

        m = MAIN_CSS_LINK.search(html)
        if not m:
            skipped.append((path, "no main.css link found"))
            continue

        html = html[: m.end()] + "\n    " + FA_LINK + html[m.end():]
        with io.open(path, "w", encoding="utf-8", newline="") as f:
            f.write(html)
        changed.append(path)

    print(f"Added Font Awesome link to {len(changed)} pages")
    for p in skipped:
        print("skipped:", p)


if __name__ == "__main__":
    sys.exit(main())
