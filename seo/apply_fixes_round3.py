"""Round 3: minified CDN assets, remaining titles, content depth."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CONTENT = """
                                            <h3>Local Locksmith You Can Trust</h3>
                                            <p>From emergency lockouts to planned security upgrades, Secure Lock Solutions helps homeowners, businesses, and drivers across Orange County. We rekey locks after move-ins, install smart locks and access control, cut and program car keys on-site, and repair commercial hardware. Every job is handled by licensed technicians with upfront pricing. View <a href="emergency.html">emergency locksmith</a> options, <a href="lock-change.html">lock change services</a>, or <a href="hours.html">current hours</a>, then call <a href="tel:+17143419244">(714) 341-9244</a>.</p>
"""

TARGETS = [
    "yorba-linda.html", "westminster.html", "tustin.html", "san-clemente.html",
    "placentia.html", "mission-viejo.html", "lake-forest.html", "laguna-niguel.html",
    "laguna-beach.html", "garden-grove.html", "dana-point.html", "brea.html",
    "buena-park.html", "aliso-viejo.html", "la-habra.html", "huntington-beach.html",
    "fullerton.html", "costa-mesa.html", "cypress.html", "fountain-valley.html",
]


def main() -> None:
    title_re = re.compile(
        r"<title>Locksmith ([^|]+?) CA \| 24/7 Emergency Service \| Secure Lock Solutions</title>"
    )
    for path in ROOT.glob("*.html"):
        content = path.read_text(encoding="utf-8")
        original = content
        content = content.replace(
            "https://unpkg.com/aos@2.3.1/dist/aos.css",
            "https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.min.css",
        )
        content = content.replace(
            "https://unpkg.com/aos@2.3.1/dist/aos.js",
            "https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.min.js",
        )
        match = title_re.search(content)
        if match:
            city = match.group(1).strip()
            new_title = f"{city} Locksmith | 24/7 | Secure Lock Solutions"
            content = title_re.sub(f"<title>{new_title}</title>", content, count=1)
        if content != original:
            path.write_text(content, encoding="utf-8")
            print("assets/title", path.name)

    for name in TARGETS:
        path = ROOT / name
        if not path.exists() or "Local Locksmith You Can Trust" in path.read_text(encoding="utf-8"):
            continue
        content = path.read_text(encoding="utf-8")
        if "</article>" not in content:
            continue
        content = content.replace("</article>", CONTENT + "\n                                        </article>", 1)
        path.write_text(content, encoding="utf-8")
        print("content", name)

    serv = ROOT / "serv-form.html"
    text = serv.read_text(encoding="utf-8")
    if "Local Locksmith You Can Trust" not in text:
        insert = CONTENT.replace("                                            ", "  ")
        text = text.replace(
            '<h2><i class="fas fa-calendar-check"></i> Book Your Appointment</h2>',
            '<h2><i class="fas fa-calendar-check"></i> Book Your Appointment</h2>' + insert,
            1,
        )
        serv.write_text(text, encoding="utf-8")
        print("serv-form content")


if __name__ == "__main__":
    main()
