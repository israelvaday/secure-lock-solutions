"""Flag any changed line that is NOT explained by the 24/7 cleanup."""
import re
import subprocess

diff = subprocess.run(
    ["git", "diff", "1ad92f9", "HEAD", "--", "*.html"],
    capture_output=True, text=True, encoding="utf-8",
).stdout

# Markers that legitimately appear in changed lines after the cleanup
EXPECTED = re.compile(
    r"24/7|Emergency|emergency|On Call|on call|Extended hours|Fast mobile|"
    r"Fast response|ready to help|respond fast|Emergency Service|"
    r"locksmith services|lockout service|Car Lockout|Business Support|"
    r"Lockout Service|availability|available\.|rancho-santa-margarita",
    re.IGNORECASE,
)

suspicious = 0
current_file = None
for line in diff.splitlines():
    if line.startswith("diff --git"):
        current_file = line.split(" b/")[-1]
    elif line.startswith(("+++", "---")):
        continue
    elif line.startswith(("+", "-")):
        content = line[1:]
        if not EXPECTED.search(content):
            suspicious += 1
            print(f"{current_file} {line[:1]} {content.strip()[:150]}")

print(f"\nSuspicious lines: {suspicious}")
