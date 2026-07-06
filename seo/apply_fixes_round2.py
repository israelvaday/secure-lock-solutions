"""Second-round Semrush fixes: llms, blog anchors, city links, content."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ORPHAN_CITIES = [
    ("villa-park.html", "Villa Park"),
    ("stanton.html", "Stanton"),
    ("seal-beach.html", "Seal Beach"),
    ("san-juan-capistrano.html", "San Juan Capistrano"),
    ("rossmoor.html", "Rossmoor"),
    ("rancho-santa-margarita.html", "Rancho Santa Margarita"),
    ("north-tustin.html", "North Tustin"),
    ("midway-city.html", "Midway City"),
    ("los-alamitos.html", "Los Alamitos"),
    ("las-flores.html", "Las Flores"),
    ("laguna-woods.html", "Laguna Woods"),
    ("laguna-hills.html", "Laguna Hills"),
    ("ladera-ranch.html", "Ladera Ranch"),
    ("coto-de-caza.html", "Coto De Caza"),
    ("la-palma.html", "La Palma"),
    ("cypress.html", "Cypress"),
]

BLOG_BUTTONS = [
    ('blog001.html" class="button">Read More', 'blog001.html" class="button">Read rekey vs replace guide'),
    ('blog002.html" class="button">Read More', 'blog002.html" class="button">Read smart lock guide'),
    ('blog003.html" class="button">Read More', 'blog003.html" class="button">Read lockout emergency guide'),
    ('blog004.html" class="button">Read More', 'blog004.html" class="button">Read home security tips'),
    ('blog005.html" class="button">Read More', 'blog005.html" class="button">Read car key guide'),
    ('emergency.html" class="button">Learn More', 'emergency.html" class="button">Emergency locksmith services'),
]

CONTENT_BLOCK = """
                                            <h3>Trusted Orange County Locksmith</h3>
                                            <p>Secure Lock Solutions is a licensed and insured locksmith based in Irvine, serving {city} and all of Orange County. Whether you are locked out, moving into a new home, or upgrading business security, our mobile technicians arrive in 15–30 minutes with the tools to solve lockouts, rekeying, lock changes, smart lock installation, and car key replacement. Call <a href="tel:+17143419244">(714) 341-9244</a> for immediate help or <a href="serv-form.html">book service online</a>. See our full <a href="service-areas.html">service area list</a> and nearby pages including <a href="irvine.html">Irvine</a>, <a href="anaheim.html">Anaheim</a>, and <a href="santa-ana.html">Santa Ana</a> locksmith services.</p>
"""

NEARBY = {
    "villa-park.html": [("orange.html", "Orange"), ("santa-ana.html", "Santa Ana"), ("tustin.html", "Tustin")],
    "stanton.html": [("westminster.html", "Westminster"), ("garden-grove.html", "Garden Grove"), ("cypress.html", "Cypress")],
    "seal-beach.html": [("los-alamitos.html", "Los Alamitos"), ("westminster.html", "Westminster"), ("huntington-beach.html", "Huntington Beach")],
    "san-juan-capistrano.html": [("laguna-niguel.html", "Laguna Niguel"), ("dana-point.html", "Dana Point"), ("mission-viejo.html", "Mission Viejo")],
    "rossmoor.html": [("los-alamitos.html", "Los Alamitos"), ("seal-beach.html", "Seal Beach"), ("westminster.html", "Westminster")],
    "rancho-santa-margarita.html": [("mission-viejo.html", "Mission Viejo"), ("lake-forest.html", "Lake Forest"), ("laguna-niguel.html", "Laguna Niguel")],
    "north-tustin.html": [("tustin.html", "Tustin"), ("orange.html", "Orange"), ("santa-ana.html", "Santa Ana")],
    "midway-city.html": [("westminster.html", "Westminster"), ("huntington-beach.html", "Huntington Beach"), ("fountain-valley.html", "Fountain Valley")],
    "los-alamitos.html": [("seal-beach.html", "Seal Beach"), ("rossmoor.html", "Rossmoor"), ("cypress.html", "Cypress")],
    "las-flores.html": [("ladera-ranch.html", "Ladera Ranch"), ("rancho-santa-margarita.html", "Rancho Santa Margarita"), ("mission-viejo.html", "Mission Viejo")],
    "laguna-woods.html": [("laguna-hills.html", "Laguna Hills"), ("irvine.html", "Irvine"), ("lake-forest.html", "Lake Forest")],
    "laguna-hills.html": [("laguna-woods.html", "Laguna Woods"), ("mission-viejo.html", "Mission Viejo"), ("lake-forest.html", "Lake Forest")],
    "ladera-ranch.html": [("las-flores.html", "Las Flores"), ("mission-viejo.html", "Mission Viejo"), ("san-juan-capistrano.html", "San Juan Capistrano")],
    "coto-de-caza.html": [("rancho-santa-margarita.html", "Rancho Santa Margarita"), ("ladera-ranch.html", "Ladera Ranch"), ("mission-viejo.html", "Mission Viejo")],
    "la-palma.html": [("cypress.html", "Cypress"), ("buena-park.html", "Buena Park"), ("anaheim.html", "Anaheim")],
    "cypress.html": [("la-palma.html", "La Palma"), ("los-alamitos.html", "Los Alamitos"), ("garden-grove.html", "Garden Grove")],
}


def fix_blog() -> None:
    path = ROOT / "blog.html"
    content = path.read_text(encoding="utf-8")
    for old, new in BLOG_BUTTONS:
        content = content.replace(old, new)
    path.write_text(content, encoding="utf-8")
    print("blog anchors fixed")


def add_index_city_links() -> None:
    path = ROOT / "index.html"
    content = path.read_text(encoding="utf-8")
    marker = '<a href="service-areas.html" class="button small alt">View All 40+ Cities →</a>'
    if marker not in content:
        return
    buttons = "".join(f'\n                  <a href="{href}" class="button small">{name}</a>' for href, name in ORPHAN_CITIES)
    content = content.replace(marker, buttons + "\n                  " + marker)
    path.write_text(content, encoding="utf-8")
    print("index city links added")


def boost_city_pages() -> None:
    for filename, city in ORPHAN_CITIES:
        path = ROOT / filename
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        if "Trusted Orange County Locksmith" in content:
            continue
        block = CONTENT_BLOCK.format(city=city)
        nearby = NEARBY.get(filename, [])
        if nearby:
            links = ", ".join(f'<a href="{h}">{n}</a>' for h, n in nearby)
            block = block.replace(
                "See our full <a href=\"service-areas.html\">service area list</a> and nearby pages including <a href=\"irvine.html\">Irvine</a>, <a href=\"anaheim.html\">Anaheim</a>, and <a href=\"santa-ana.html\">Santa Ana</a> locksmith services.",
                f"Nearby areas we also serve: {links}. Browse our full <a href=\"service-areas.html\">Orange County service areas</a>.",
            )
        content = content.replace("</article>", block + "\n                                        </article>", 1)
        path.write_text(content, encoding="utf-8")
        print("content", filename)


def boost_thin_pages() -> None:
    targets = ["service-areas.html", "serv-form.html", "placentia.html", "westminster.html", "yorba-linda.html", "tustin.html", "stanton.html", "san-clemente.html", "rossmoor.html", "orange.html"]
    block = """
                                            <h3>Why Choose Secure Lock Solutions?</h3>
                                            <p>We are a California licensed locksmith (License #LCO8500) based at 1100 Synergy in Irvine. Our team handles emergency lockouts, lock rekeying, high-security hardware, access control, and automotive key services across Orange County with transparent pricing and fast mobile response. Explore our <a href="residential.html">residential</a>, <a href="commercial.html">commercial</a>, and <a href="automotive.html">automotive</a> services, read our <a href="blog.html">security blog</a>, or call <a href="tel:+17143419244">(714) 341-9244</a> now.</p>
"""
    for name in targets:
        path = ROOT / name
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        if "Why Choose Secure Lock Solutions?" in content:
            continue
        if "</article>" in content:
            content = content.replace("</article>", block + "\n                                        </article>", 1)
        elif '<div id="content">' in content:
            content = content.replace('<div id="content">', '<div id="content">' + block, 1)
        else:
            continue
        path.write_text(content, encoding="utf-8")
        print("thin", name)


def main() -> None:
    fix_blog()
    add_index_city_links()
    boost_city_pages()
    boost_thin_pages()


if __name__ == "__main__":
    main()
