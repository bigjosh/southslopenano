"""One-shot probe of all IMAP folders so we can spot mail being silently
routed to Junk/Spam/Trash. Reads config from inbox/config.json."""
import json, imaplib, sys
from pathlib import Path

cfg = json.loads(Path(__file__).parent.joinpath('config.json').read_text())
M = imaplib.IMAP4_SSL(cfg['imap_host'])
M.login(cfg['imap_user'], cfg['imap_pass'])
typ, data = M.list()
if typ != 'OK':
    print('LIST failed:', data); sys.exit(1)
folders = []
for raw in data:
    s = raw.decode(errors='replace')
    # mailbox name is the last token, possibly quoted
    name = s.split(' "/" ')[-1].strip().strip('"')
    folders.append(name)
print(f'Folders ({len(folders)}):')
for f in folders:
    try:
        typ, d = M.select(f'"{f}"', readonly=True)
        if typ != 'OK':
            print(f'  {f}: select fail')
            continue
        msgcount = int(d[0])
        typ, d = M.uid('SEARCH', None, 'ALL')
        uids = d[0].split() if typ == 'OK' and d[0] else []
        print(f'  {f}: {msgcount} total, {len(uids)} via UID search')
    except Exception as e:
        print(f'  {f}: error {e!r}')
M.logout()
