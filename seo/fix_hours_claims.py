"""Fix remaining inaccurate round-the-clock claims in footers and body copy.

Actual hours: Sun-Thu 24h, Fri until 1:00 PM, Sat closed. These claims
('24 Hours / 7 Days a Week', 'around the clock', '24 hours a day') all
contradict that. Replacements preserve line endings (newline='').
"""
import glob
import io
import sys

FIXES = [
    # Footer hours block (5 city pages)
    (
        "<dd>24 Hours / 7 Days a Week<br>Emergency Service Always Available</dd>",
        "<dd>Sun - Thu: Open 24 Hours<br>Fri: Until 1:00 PM, Sat: Closed</dd>",
    ),
    # Body copy
    (
        "We respond fast throughout Orange County, 24 hours a day, 7 days a week.",
        "We respond fast throughout Orange County.",
    ),
    (
        "locksmith services 24 hours a day throughout Huntington Beach",
        "locksmith services throughout Huntington Beach",
    ),
    (
        "available around the clock for emergency lockouts",
        "available for emergency lockouts",
    ),
    (
        "available around the clock and typically arrive",
        "on call and typically arrive",
    ),
    (
        "provides fast, damage-free car lockout service 24 hours a day, 7 days a week.",
        "provides fast, damage-free car lockout service.",
    ),
    (
        "California\u201424 hours a day, 7 days a week, 365 days a year.",
        "California\u2014with fast response when you need it most.",
    ),
    (
        "emergency locksmith services available around the clock.",
        "emergency locksmith services.",
    ),
    (
        "we provide fast, professional locksmith services 24 hours a day.",
        "we provide fast, professional locksmith services.",
    ),
]


def main() -> None:
    changed = []
    misses = []
    for path in sorted(glob.glob("*.html")):
        with io.open(path, "r", encoding="utf-8", newline="") as f:
            html = f.read()
        original = html
        for old, new in FIXES:
            html = html.replace(old, new)
        if html != original:
            with io.open(path, "w", encoding="utf-8", newline="") as f:
                f.write(html)
            changed.append(path)

    # Verify every fix landed somewhere
    all_html = ""
    for path in sorted(glob.glob("*.html")):
        all_html += io.open(path, encoding="utf-8", newline="").read()
    for old, _ in FIXES:
        if old in all_html:
            misses.append(old[:60])

    print(f"Updated {len(changed)} files:")
    for p in changed:
        print(" -", p)
    print("Fixes that did NOT land:", misses if misses else "none")


if __name__ == "__main__":
    sys.exit(main())
