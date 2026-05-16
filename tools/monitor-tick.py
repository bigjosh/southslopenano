"""One-shot Phase 1 monitor tick. Pulls and prints the four things
worth checking each hour:

  1. Live parcel count.
  2. Mosaic code state (any new external requests?).
  3. Flask inbox pending count.
  4. The diff against the previous tick (so we can spot a delta fast).

Snapshots are written to tools/.monitor-ticks.jsonl so each invocation
appends a structured record and prints a human-readable delta. Run from
the repo root.
"""

import json, sys, time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / 'tools' / '.monitor-ticks.jsonl'

PARCELS_URL = 'https://mosaic.southslopenano.com/upload/cgi-bin/app.py?command=get-parcels'
CODES_URL   = 'https://mosaic.southslopenano.com/upload/cgi-bin/app.py?command=get-codes&admin-id=mosaicisnice'
INBOX_URL   = 'http://localhost:5000/'

INTERNAL_BACKERS = {'mosaic@southslopenano.com', 'bigjosh@gmail.com'}
INTERNAL_DOMAINS = ('joshreply.com',)


def fetch_json(url):
    try:
        with urlopen(Request(url, headers={'User-Agent': 'monitor-tick'}), timeout=15) as r:
            return json.loads(r.read().decode('utf-8'))
    except (URLError, Exception) as e:
        return {'error': str(e)}


def fetch_text(url):
    try:
        with urlopen(Request(url, headers={'User-Agent': 'monitor-tick'}), timeout=10) as r:
            return r.read().decode('utf-8', errors='replace')
    except (URLError, Exception) as e:
        return f'(unreachable: {e})'


def is_external(backer):
    b = (backer or '').lower()
    if b in INTERNAL_BACKERS:
        return False
    if any(d in b for d in INTERNAL_DOMAINS):
        return False
    return True


def gather():
    parcels = fetch_json(PARCELS_URL)
    parcel_count = len(parcels.get('parcels', []))

    codes_resp = fetch_json(CODES_URL)
    codes = codes_resp.get('codes', [])
    mosaic = [c for c in codes if 'mosaic' in str(c.get('notes','')).lower()
              or any(a in str(c.get('backer-id','')).lower()
                     for a in ['sapphire@', 'pixel@', 'tile@', 'lockin@',
                               'foundry@', 'etch@', 'jb-mosaic@', 'mosaic@'])]
    external_codes = [c for c in mosaic if is_external(c.get('backer-id', ''))]
    uploaded_external = [c for c in external_codes if c.get('status') == 'uploaded']

    inbox_html = fetch_text(INBOX_URL)
    import re
    m = re.search(r'Pending requests <span class="text-secondary">\((\d+)\)', inbox_html)
    pending = int(m.group(1)) if m else None

    return {
        'ts': int(time.time()),
        'parcels': parcel_count,
        'codes_total': len(codes),
        'mosaic_codes': len(mosaic),
        'external_codes': len(external_codes),
        'external_uploaded': len(uploaded_external),
        'inbox_pending': pending,
        'external_backers': [c.get('backer-id') for c in external_codes],
    }


def previous():
    if not LOG.exists(): return None
    lines = LOG.read_text(encoding='utf-8').strip().splitlines()
    if not lines: return None
    try:
        return json.loads(lines[-1])
    except json.JSONDecodeError:
        return None


def append(rec):
    LOG.parent.mkdir(exist_ok=True)
    with LOG.open('a', encoding='utf-8') as f:
        f.write(json.dumps(rec) + '\n')


def main():
    cur = gather()
    prev = previous()
    append(cur)

    print(f"=== monitor tick @ {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(cur['ts']))} ===")
    print(f"  tiles filled       : {cur['parcels']} / 1124"
          + (f"  (Δ +{cur['parcels'] - prev['parcels']})" if prev else ""))
    print(f"  Mosaic-tagged codes: {cur['mosaic_codes']}"
          + (f"  (Δ +{cur['mosaic_codes'] - prev['mosaic_codes']})" if prev else ""))
    print(f"  External requests  : {cur['external_codes']}"
          + (f"  (Δ +{cur['external_codes'] - prev['external_codes']})" if prev else ""))
    print(f"  External uploaded  : {cur['external_uploaded']}"
          + (f"  (Δ +{cur['external_uploaded'] - prev['external_uploaded']})" if prev else ""))
    print(f"  Inbox pending      : {cur['inbox_pending']}")
    if cur['external_backers']:
        print(f"  External backers   : {cur['external_backers']}")


if __name__ == '__main__':
    main()
