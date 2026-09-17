"""Check every Blind 75 entry in catalog.py against LeetCode's public API.

Needs network access. Not part of ./check all, because CI shouldn't depend on
LeetCode being reachable. Run it after editing the catalog:

    python3 tools/verify_catalog.py
"""
import json
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from catalog import BLIND_75  # noqa: E402

QUERY = ("query q($s: String!) { question(titleSlug: $s) "
         "{ questionFrontendId title difficulty isPaidOnly } }")


def fetch(slug):
    body = json.dumps({"query": QUERY, "variables": {"s": slug}}).encode()
    req = urllib.request.Request(
        "https://leetcode.com/graphql", data=body,
        headers={"Content-Type": "application/json",
                 "Referer": "https://leetcode.com", "User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)["data"]["question"]


def main():
    problems = 0
    for module, lc_id, title, slug, difficulty, premium in BLIND_75:
        q = fetch(slug)
        if q is None:
            print(f"  NOT FOUND  {slug}")
            problems += 1
            continue
        got = (int(q["questionFrontendId"]), q["title"], q["difficulty"], q["isPaidOnly"])
        want = (lc_id, title, difficulty, premium)
        if got != want:
            print(f"  MISMATCH   {slug}\n    catalog: {want}\n    leetcode: {got}")
            problems += 1
        time.sleep(0.25)
    total = len(BLIND_75)
    print(f"{total - problems}/{total} entries match LeetCode")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
