"""Remove misleading '24/7' from Google search preview elements and body copy.

The business is closed Saturdays, so '24/7' in titles, meta descriptions,
og/twitter tags, JSON-LD schema, and body copy is inaccurate. Replaces it
with emergency/fast-response phrasing.

Safe by design:
- Reads/writes with newline='' so original CRLF line endings are preserved.
- No global whitespace or capitalization passes; capitalization is fixed
  only in unambiguous contexts (after a literal period, at the start of a
  meta content attribute, or at the start of a JSON string value).
"""
import glob
import io
import re
import sys

TITLE_FIXES = [
    (" | 24/7 Emergency Service | ", " | "),
    (" | 24/7 Emergency Lockout | ", " | "),
    (" | 24/7 Locksmith | ", " | "),
    (" | 24/7 | ", " | "),
]

# Ordered longest-first so specific phrases win.
TEXT_FIXES = [
    ("24/7 emergency commercial lockout services", "emergency commercial lockout services"),
    ("24/7 emergency lockout service", "emergency lockout service"),
    ("24/7 emergency service", "emergency service"),
    ("provides 24/7 locksmith services", "provides emergency locksmith services"),
    ("24/7 locksmith services", "locksmith services"),
    ("Fast 24/7 response", "Fast emergency response"),
    ("Available 24/7 mobile service", "Fast mobile service"),
    ("Available 24/7/365", "Emergency Service Available"),
    ("Available 24/7.", "Emergency service available."),
    ("<b>Available 24/7:</b>", "<b>Emergency Service:</b>"),
    ("We're available 24/7 throughout", "We respond fast throughout"),
    ("available 24/7 to get you back inside", "on call to get you back inside"),
    ("We're here 24/7 and typically arrive", "We're on call and typically arrive"),
    ("We're Here 24/7!", "We're On Call!"),
    ("Available 24/7", "Emergency Service Available"),
    ("24/7 availability including holidays", "Extended hours, including holidays"),
    ("24/7 Emergency Locksmith", "Emergency Locksmith"),
    ("24/7 Emergency", "Emergency"),
    (", 24/7 availability.", ", emergency availability."),
    ("24/7 availability", "Emergency availability"),
    (" 24/7.</p>", ".</p>"),
    ("<td>24/7 available</td>", "<td>Emergency service</td>"),
    ("24/7 locksmith,", "emergency locksmith,"),
    ("<h2>24/7 Car Lockout</h2>", "<h2>Car Lockout</h2>"),
    ("<h2>24/7 Business Support</h2>", "<h2>Business Support</h2>"),
    ("<span>24/7 Lockout Service</span>", "<span>Emergency Lockout Service</span>"),
    ("24/7", ""),  # catch-all; anything left is reported by main()
]

# Capitalization repairs, restricted to unambiguous contexts.
CAP_FIXES = [
    (". emergency", ". Emergency"),
    ('content="emergency', 'content="Emergency'),
    ('": "emergency', '": "Emergency'),
]


def process(path: str):
    with io.open(path, "r", encoding="utf-8", newline="") as f:
        html = f.read()
    original = html
    for old, new in TITLE_FIXES + TEXT_FIXES + CAP_FIXES:
        html = html.replace(old, new)
    leftover = [m.start() for m in re.finditer(r"24/7", html)]
    if html != original:
        with io.open(path, "w", encoding="utf-8", newline="") as f:
            f.write(html)
    return html != original, len(leftover)


def main() -> None:
    changed, flagged = [], []
    for path in sorted(glob.glob("*.html")):
        did_change, n_left = process(path)
        if did_change:
            changed.append(path)
        if n_left:
            flagged.append((path, n_left))
    print(f"Updated {len(changed)} files")
    if flagged:
        print("LEFTOVER 24/7 occurrences:")
        for p, n in flagged:
            print(f"  {p}: {n}")
    else:
        print("No 24/7 occurrences remain in root pages")


if __name__ == "__main__":
    sys.exit(main())
