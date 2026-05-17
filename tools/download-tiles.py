"""One-shot snapshot of all currently-filled tiles on the disk.

The live viewer at https://mosaic.southslopenano.com/ serves tiles as
PNGs at https://mosaic.southslopenano.com/world/images/6/{x}/{y}.png
in a 38x38 Leaflet-style grid (zoom level 6 is native resolution).
Filled tiles return 200; empty cells return 404.

We iterate all (x,y) coords at z=6, save the 200s into docs/tiles/,
and emit docs/tiles/manifest.json listing the filenames for the
social-proof grid on the landing pages.

Idempotent: re-run any time. Existing tile files are overwritten.
Manifest is regenerated from the filesystem.
"""

import json
import sys
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TILES_DIR = ROOT / "docs" / "tiles"
MANIFEST = TILES_DIR / "manifest.json"

BASE = "https://mosaic.southslopenano.com/world/images/6/{x}/{y}.png"
GRID_SIZE = 38  # 38x38 tile grid at native zoom
BLANK_THRESHOLD = 200  # bytes — empty cells return a ~70B placeholder PNG


def fetch_tile(x, y):
    """Return PNG bytes for filled cells, None for blanks/missing."""
    url = BASE.format(x=x, y=y)
    req = urllib.request.Request(url, headers={"User-Agent": "mosaic-tile-snapshot"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            if r.status != 200:
                return None
            data = r.read()
            # Empty cells return a tiny placeholder PNG; only keep real content.
            return data if len(data) >= BLANK_THRESHOLD else None
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        print(f"  ! {x},{y}: HTTP {e.code}", file=sys.stderr)
    except Exception as e:
        print(f"  ! {x},{y}: {e}", file=sys.stderr)
    return None


def main():
    TILES_DIR.mkdir(parents=True, exist_ok=True)
    saved = []
    checked = 0
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            checked += 1
            data = fetch_tile(x, y)
            if data is None:
                continue
            name = f"x{x:02d}_y{y:02d}.png"
            (TILES_DIR / name).write_bytes(data)
            saved.append(name)
            if len(saved) % 20 == 0:
                print(f"  saved {len(saved)} so far (last: {name})")
    saved.sort()
    MANIFEST.write_text(json.dumps(saved, indent=2), encoding="utf-8")
    print()
    print(f"Done. Checked {checked} cells, saved {len(saved)} tiles to {TILES_DIR}.")
    print(f"Manifest: {MANIFEST}")


if __name__ == "__main__":
    main()
