"""Wire a StatCounter click-event tracker into the 8 variant pages.

The trick: our landing pages set referrerpolicy=no-referrer at the
meta level, which strips Referer from any tracking image. StatCounter
then can't tell which page fired the pixel and shows "unknown".
We work around it by:

  1. Setting referrerPolicy=unsafe-url on the dynamic <img> so it
     sends Referer despite the page-level meta.
  2. history.replaceState() to a URL with ?event=<name> just before
     firing the pixel, then restoring the URL on image load/error.
     This makes the Referer that StatCounter sees include the event
     tag, so the click logs as a distinct page in the Activity feed.

The exposed window.trackEvent(name) function lets us tag any future
button presses by calling trackEvent('whatever') from another handler.

Idempotent — re-running replaces any previous tracker block.
"""

import re
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / 'docs'

OLD_BLOCK_RE = re.compile(
    r'\n*<script>\s*\n//\s*cta-click tracker[\s\S]*?</script>\n*',
    re.MULTILINE,
)

SCRIPT = """
<script>
// cta-click tracker v2 — replaceState + unsafe-url Referer override
// so StatCounter logs each click as /<page>?event=<name>.
(function() {
  var variant = (location.pathname.split('/').pop() || 'home').replace(/\\.html$/, '') || 'home';
  function trackEvent(name) {
    if (!window.history || !history.replaceState) return;
    var orig = location.pathname + location.search + location.hash;
    var fake = location.pathname + '?event=' + encodeURIComponent(name);
    try { history.replaceState(null, '', fake); } catch (e) { return; }
    var img = new Image();
    img.referrerPolicy = 'unsafe-url';
    var restore = function() {
      try { history.replaceState(null, '', orig); } catch (e) {}
    };
    img.onload = restore;
    img.onerror = restore;
    img.src = 'https://c.statcounter.com/13233744/0/be0b9727/1/?_=' + Date.now();
  }
  window.trackEvent = trackEvent;
  document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('a.cta-button[href^="mailto:"], a.fine[href^="mailto:"]').forEach(function(a) {
      a.addEventListener('click', function() {
        trackEvent('mailto-click-' + variant);
      });
    });
  });
})();
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
