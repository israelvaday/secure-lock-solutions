"""Launch Semrush Site Audit, poll until done, print issue summary."""
from __future__ import annotations

import json
import os
import sys
import time
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

KEY = os.environ.get("SEMRUSH_API_KEY", "").strip()
PID = os.environ.get("SEMRUSH_PROJECT_ID", "30305811")
BASE = f"https://api.semrush.com/reports/v1/projects/{PID}/siteaudit"


def get(url: str) -> dict | list:
    req = Request(url, headers={"User-Agent": "sls-audit-loop/1"})
    with urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def post(url: str) -> dict:
    req = Request(url, method="POST", headers={"User-Agent": "sls-audit-loop/1"})
    with urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    if not KEY:
        print("Set SEMRUSH_API_KEY", file=sys.stderr)
        return 1

    print(f"Launching audit for project {PID}...")
    try:
        launched = post(f"{BASE}/launch?key={KEY}")
        print("Launch:", launched)
    except HTTPError as e:
        print("Launch failed:", e.read().decode(), file=sys.stderr)
        return 1

    for i in range(120):
        info = get(f"{BASE}/info?key={KEY}")
        status = info.get("status")
        print(
            f"[{i:02d}] status={status} errors={info.get('errors')} "
            f"warnings={info.get('warnings')} notices={info.get('notices')} "
            f"crawled={info.get('running_pages_crawled') or info.get('pages_crawled')}",
            flush=True,
        )
        if status == "FINISHED":
            break
        time.sleep(30)

    info = get(f"{BASE}/info?key={KEY}")
    snap = info.get("current_snapshot", {}).get("snapshot_id")
    if not snap:
        snaps = get(f"{BASE}/snapshots?key={KEY}")
        snap = snaps["snapshots"][0]["snapshot_id"]

    meta = get(f"{BASE}/meta/issues?key={KEY}")
    issues = {i["id"]: i.get("title", "") for i in meta.get("issues", [])}
    defects = info.get("defects", {})

    print("\n=== AUDIT RESULT ===")
    print(f"errors={info.get('errors')} warnings={info.get('warnings')} notices={info.get('notices')}")
    print(f"pages_crawled={info.get('pages_crawled')}")
    for iid, count in sorted(defects.items(), key=lambda x: -x[1]):
        title = issues.get(int(iid), f"Issue {iid}")
        print(f"  {iid}: {count:4d}  {title}")

    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "audit_info.json"), "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2)

    priority = [2, 45, 103, 106, 137, 203, 207, 102, 117, 213, 217, 122, 135, 205]
    for iid in priority:
        if not defects.get(str(iid)) and not defects.get(iid):
            continue
        qs = urlencode({"key": KEY, "limit": 10})
        data = get(f"{BASE}/snapshot/{snap}/issue/{iid}?{qs}")
        print(f"\n--- {iid} {issues.get(iid, '')} ({data.get('total')}) ---")
        for row in data.get("data", [])[:10]:
            url = row.get("source_url") or row.get("target_url") or ""
            extra = row.get("info") or row.get("title") or ""
            print(f"  {url}  {extra}")

    return 0 if info.get("errors", 99) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
