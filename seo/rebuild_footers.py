"""Rebuild the footer on every page with a rich 4-column layout.

- Fixes broken grid (empty col-3 placeholder, 3x col-6 = 150% width),
  invalid nested <ul>, and missing copyright.
- Adds About / Services / Service Areas / Contact columns.
- Preserves each page's existing 'Service Area' text (city-specific).
- Accurate hours everywhere: Sun-Thu 24h, Fri until 1 PM, Sat closed.
- Reads/writes with newline='' to preserve CRLF line endings.
"""
import glob
import io
import re
import sys

FOOTER_TEMPLATE = """<footer id="footer" class="container" data-aos="fade-up">
                    <div class="footer-grid">
                        <section class="footer-col">
                            <h2>Secure Lock Solutions</h2>
                            <p class="footer-about">Licensed &amp; insured mobile locksmiths serving all of Orange County, CA. Fast response for homes, businesses, and vehicles — lockouts, rekeys, car keys, smart locks, and more.</p>
                            <ul class="icons">
                                <li><a href="https://www.instagram.com/secur_elock?igsh=ZzI2cmJoeXFsM2dm&utm_source=qr" class="instagram" target="_blank" rel="noopener"><i class="fab fa-instagram"></i></a></li>
                            </ul>
                        </section>
                        <section class="footer-col">
                            <h2>Services</h2>
                            <ul class="footer-links">
                                <li><a href="emergency.html">Emergency Lockout</a></li>
                                <li><a href="residential.html">Residential Locksmith</a></li>
                                <li><a href="commercial.html">Commercial Locksmith</a></li>
                                <li><a href="automotive.html">Automotive Locksmith</a></li>
                                <li><a href="smart-locks.html">Smart Locks</a></li>
                                <li><a href="lock-change.html">Lock Change &amp; Rekey</a></li>
                                <li><a href="key-duplication.html">Key Duplication</a></li>
                                <li><a href="safe-services.html">Safe Services</a></li>
                            </ul>
                        </section>
                        <section class="footer-col">
                            <h2>Service Areas</h2>
                            <ul class="footer-links">
                                <li><a href="anaheim.html">Anaheim</a></li>
                                <li><a href="irvine.html">Irvine</a></li>
                                <li><a href="santa-ana.html">Santa Ana</a></li>
                                <li><a href="huntington-beach.html">Huntington Beach</a></li>
                                <li><a href="newport-beach.html">Newport Beach</a></li>
                                <li><a href="costa-mesa.html">Costa Mesa</a></li>
                                <li><a href="service-areas.html">View All 40+ Cities &rarr;</a></li>
                            </ul>
                        </section>
                        <section class="footer-col">
                            <h2>Get in Touch</h2>
                            <dl class="contact">
                                <dt>Phone</dt>
                                <dd><a href="tel:+17143419244">(714) 341-9244</a></dd>
                                <dt>Email</dt>
                                <dd><a href="mailto:securelocksmithsolution@gmail.com">securelocksmithsolution@gmail.com</a></dd>
                                <dt>Address</dt>
                                <dd>1100 Synergy<br>Irvine, CA 92614</dd>
                                <dt>Hours</dt>
                                <dd>Sun &ndash; Thu: Open 24 hours<br>Fri: 12:00 AM &ndash; 1:00 PM<br>Sat: Closed</dd>
                                <dt>Service Area</dt>
                                <dd>{service_area}</dd>
                            </dl>
                        </section>
                    </div>
                    <div class="footer-bottom">
                        <ul class="menu">
                            <li><a href="service-areas.html">Service Areas</a></li>
                            <li><a href="hours.html">Hours</a></li>
                            <li><a href="blog.html">Blog</a></li>
                            <li><a href="gallery.html">Gallery</a></li>
                            <li><a href="serv-form.html">Book Service</a></li>
                        </ul>
                        <p class="footer-license"><i class="fas fa-shield-alt"></i> California Licensed Locksmith | License #LCO8500 | Bureau of Security &amp; Investigative Services</p>
                        <p class="footer-copy">&copy; 2026 Secure Lock Solutions. All rights reserved.</p>
                    </div>
                </footer>"""

FOOTER_RE = re.compile(r'<footer id="footer".*?</footer>', re.DOTALL)
SERVICE_AREA_RE = re.compile(
    r"<dt>Service Area</dt>\s*<dd>(.*?)</dd>", re.DOTALL
)


def extract_service_area(html: str) -> str:
    m = SERVICE_AREA_RE.search(html)
    if not m:
        return "Orange County, California"
    text = re.sub(r"<[^>]+>", " ", m.group(1))
    return re.sub(r"\s+", " ", text).strip()


def main() -> None:
    changed, skipped = [], []
    for path in sorted(glob.glob("*.html")):
        with io.open(path, "r", encoding="utf-8", newline="") as f:
            html = f.read()
        matches = FOOTER_RE.findall(html)
        if len(matches) != 1:
            skipped.append((path, len(matches)))
            continue
        area = extract_service_area(html)
        new_footer = FOOTER_TEMPLATE.format(service_area=area)
        html = FOOTER_RE.sub(lambda _: new_footer, html, count=1)
        with io.open(path, "w", encoding="utf-8", newline="") as f:
            f.write(html)
        changed.append((path, area))

    print(f"Rebuilt footer on {len(changed)} pages")
    for p, area in changed:
        print(f" - {p}  [area: {area}]")
    if skipped:
        print("SKIPPED (footer count != 1):")
        for p, n in skipped:
            print(f" - {p}: {n} footers")


if __name__ == "__main__":
    sys.exit(main())
