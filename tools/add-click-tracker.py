"""Add a small JS click handler that fires a StatCounter pixel on
mailto-button clicks. The pixel uses a custom path so each click
appears as a distinct entry in StatCounter's pageload log, tagged
with the variant slug (sapphire, pixel, tile, etc.).

Idempotent — skips files that already contain the marker comment.
"""

from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / 'docs'
MARKER = 'cta-click tracker'

# Each variant page gets the same handler — the variant name is
# derived at runtime from location.pathname.
SCRIPT = """
<script>
// cta-click tracker — fires a StatCounter pixel when the mailto
// CTA is clicked. Logs as a distinct pageview path per variant.
(function() {
  var variant = (location.pathname.split('/').pop() || 'home').replace(/\\.html$/, '') || 'home';
  document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('a.cta-button[href^="mailto:"], a.fine[href^="mailto:"]').forEach(function(a) {
      a.addEventListener('click', function() {
        new Image().src = 'https://c.statcounter.com/13233744/0/be0b9727/1/'
          + '?u=' + encodeURIComponent('/cta-click/' + variant)
          + '&t=' + encodeURIComponent('cta-click-' + variant)
          + '&r=' + encodeURIComponent(location.href)
          + '&_=' + Date.now();
      });
    });
  });
})();
</script>
"""

# Only the 8 variant pages have a CTA. The home page does not, so we
# skip it — adding a handler there would be a no-op.
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
        if MARKER in text:
            print(f'  {name:<16} skip (already wired)')
            continue
        if '</body>' not in text:
            print(f'  {name:<16} ERROR no </body>')
            continue
        new = text.replace('</body>', SCRIPT + '</body>', 1)
        path.write_text(new, encoding='utf-8')
        print(f'  {name:<16} OK')


if __name__ == '__main__':
    main()
