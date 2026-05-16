"""Inject the StatCounter snippet before </body> on every public-facing
HTML in docs/. One-shot script; idempotent (skips files that already
contain the project id)."""

from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / 'docs'
PROJECT_ID = '13233744'

SNIPPET = """
<!-- Default Statcounter code for SSN
https://southslopenano.com/ -->
<script type="text/javascript">
var sc_project=13233744;
var sc_invisible=1;
var sc_security="be0b9727";
</script>
<script type="text/javascript"
src="https://www.statcounter.com/counter/counter.js"
async></script>
<noscript><div class="statcounter"><a title="Web Analytics"
href="https://statcounter.com/" target="_blank"><img
class="statcounter"
src="https://c.statcounter.com/13233744/0/be0b9727/1/"
alt="Web Analytics"
referrerPolicy="no-referrer-when-downgrade"></a></div></noscript>
<!-- End of Statcounter Code -->
"""

PAGES = [
    'index.html',
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
        if PROJECT_ID in text:
            print(f'  {name:<16} skip (already has snippet)')
            continue
        if '</body>' not in text:
            print(f'  {name:<16} ERROR no </body>')
            continue
        new = text.replace('</body>', SNIPPET + '</body>', 1)
        path.write_text(new, encoding='utf-8')
        print(f'  {name:<16} OK')


if __name__ == '__main__':
    main()
