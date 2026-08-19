"""Convert all referenced raster images to WebP and update references.

- Resolves refs against images/ and assets/css/images/ (template CSS uses
  relative paths from the css folder).
- Writes .webp next to the original; originals stay on disk.
- Updates relative references in HTML/CSS. Absolute URLs
  (https://...com/images/...) are NOT touched, so og:image / twitter:image
  keep the JPG/PNG originals for social-crawler compatibility.
"""
import glob
import io
import os
import re
import sys

from PIL import Image

QUALITY = 82

REF_PATTERNS = [
    re.compile(r'(?:src|href)="(images/[^"]+?\.(?:png|jpe?g))"', re.IGNORECASE),
    re.compile(r'url\("?(images/[^")]+?\.(?:png|jpe?g))"?\)', re.IGNORECASE),
    re.compile(r'content="(?:https://securelocksmithsolution\.com/)?(images/[^"]+?\.(?:png|jpe?g))"', re.IGNORECASE),
]

SOURCE_FILES = sorted(glob.glob("*.html")) + sorted(glob.glob("assets/css/*.css"))


def collect_refs():
    refs = set()
    for path in SOURCE_FILES:
        text = io.open(path, encoding="utf-8", newline="").read()
        for pat in REF_PATTERNS:
            for m in re.finditer(pat, text):
                refs.add(m.group(m.lastindex))
    return refs


def resolve(ref):
    if os.path.exists(ref):
        return ref
    alt = os.path.join("assets/css", ref)
    if os.path.exists(alt):
        return alt
    return None


def main() -> None:
    refs = sorted(collect_refs())
    converted = {}  # ref -> (orig_bytes, webp_bytes)
    missing = []

    for ref in refs:
        src = resolve(ref)
        if not src:
            missing.append(ref)
            continue
        dst = os.path.splitext(src)[0] + ".webp"
        img = Image.open(src)
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA" if "transparency" in img.info else "RGB")
        img.save(dst, "WEBP", quality=QUALITY, method=6)
        converted[ref] = (os.path.getsize(src), os.path.getsize(dst))

    # Update references: relative refs only; absolute URLs (og:image) keep originals
    for path in SOURCE_FILES:
        text = io.open(path, encoding="utf-8", newline="").read()
        original = text
        for ref in converted:
            webp_ref = os.path.splitext(ref)[0] + ".webp"
            pat = re.compile(r"(?<!com/)" + re.escape(ref) + r"(?=[\"')])", re.IGNORECASE)
            text = pat.sub(webp_ref, text)
        if text != original:
            io.open(path, "w", encoding="utf-8", newline="").write(text)

    total_orig = sum(o for o, _ in converted.values())
    total_webp = sum(w for _, w in converted.values())
    print(f"Converted {len(converted)} images: {total_orig/1e6:.1f} MB -> {total_webp/1e6:.1f} MB "
          f"({100 * (1 - total_webp / total_orig):.0f}% smaller)")
    if missing:
        print("Referenced but file not found:")
        for m in missing:
            print(" -", m)


if __name__ == "__main__":
    sys.exit(main())
