"""Wire StatCounter's native record_click() into the 8 variant pages.

counter.js exposes `_statcounter.record_click(projectId, url)` —
logs to their Exit Links / outbound-click report. Cleaner than
firing a raw pixel: they handle session, security, deduplication.

For future button types, expose window.trackEvent(name) which calls
record_click with a `event:name` identifier. Per-variant attribution
falls out because each page passes its own mailto URL (sapphire@,
pixel@, tile@, etc.) — Exit Links groups by destination URL.

Idempotent — replaces any prior tracker block.
"""

import re
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / 'docs'
PROJECT_ID = 13233744

OLD_BLOCK_RE = re.compile(
    r'\n*<script>\s*\n//\s*cta-click tracker[\s\S]*?</script>\n*',
    re.MULTILINE,
)

SCRIPT = f"""
<script>
// cta-click tracker v3 — uses StatCounter's native record_click API
// so the click logs to Exit Links naturally (no Referer hacks).
(function() {{
  function fire(url) {{
    if (window._statcounter && _statcounter.record_click) {{
      try {{ _statcounter.record_click({PROJECT_ID}, url); }} catch (e) {{}}
    }}
  }}
  window.trackEvent = function(name) {{ fire('event:' + name); }};
  document.addEventListener('DOMContentLoaded', function() {{
    document.querySelectorAll('a.cta-button[href^="mailto:"], a.fine[href^="mailto:"]').forEach(function(a) {{
      a.addEventListener('click', function() {{ fire(a.href); }});
    }});
  }});
}})();
</script>
"""

PAGES = [
    'mosaic.html',
    'sapphire.html', 'pixel.html', 'tile.html', 'lockin.html',
    'foundry.html', 'etch.html', 'jb-mosaic.html',
]


def main():
    for name in PAGES:
        path = DOCS / name
        if not path.exists():
            print(f'  {name:<16} MISSING')
            continue
        text = path.read_text(encoding='utf-8')
        new_text, n_replaced = OLD_BLOCK_RE.subn('', text)
        if '</body>' not in new_text:
            print(f'  {name:<16} ERROR no </body>')
            continue
        new_text = new_text.replace('</body>', SCRIPT + '</body>', 1)
        if new_text == text:
            print(f'  {name:<16} unchanged')
            continue
        path.write_text(new_text, encoding='utf-8')
        print(f'  {name:<16} OK ({"replaced" if n_replaced else "inserted"})')


if __name__ == '__main__':
    main()
