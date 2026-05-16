"""Apply conversion-fix edits across all 8 variant landing pages.

Three changes per file:
1. Soften the upload-description ask (make it optional, not a demand).
2. Drop the prefilled `body=I plan to upload: ` from the mailto so the email
   opens with a blank body — less pressure to compose a sentence.
3. Add a plaintext fallback line below the CTA pointing at the raw email
   address, for mobile users whose mailto handler isn't configured.

Each variant has its own mailto alias (sapphire@, pixel@, tile@, …), so
the script extracts the alias from the existing mailto href and reuses it
for the fallback line.
"""

import re, sys
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / 'docs'
VARIANTS = ['sapphire', 'pixel', 'tile', 'lockin', 'foundry', 'etch', 'jb-mosaic', 'mosaic']

OLD_INSTRUCT = (
    "<p>To request an upload link, send us an email. In the body, "
    "briefly mention what you plan to upload. This is mostly for spam "
    "control, but we're also excited to hear your ideas.</p>"
)
NEW_INSTRUCT = (
    "<p>Send us a quick email and we'll reply with your upload link. "
    "Tell us about your idea if you want — we love seeing what people "
    "are planning.</p>"
)


def patch(path: Path, alias: str) -> tuple[bool, list[str]]:
    text = path.read_text(encoding='utf-8')
    changes = []

    if OLD_INSTRUCT in text:
        text = text.replace(OLD_INSTRUCT, NEW_INSTRUCT)
        changes.append('softened upload-description ask')

    body_prefill = '&body=I%20plan%20to%20upload%3A%20'
    if body_prefill in text:
        text = text.replace(body_prefill, '')
        changes.append('dropped body= prefill')

    cta_href = f'mailto:{alias}@southslopenano.com?subject=Mosaic%20upload%20link%20request'
    fallback_marker = f'<p class="fine center">Or write directly to'
    if fallback_marker not in text:
        cta_button_close = f'>Send your email request</a>\n    </p>'
        new_block = (
            cta_button_close
            + '\n\n    <p class="fine center">Or write directly to '
            + f'<a href="mailto:{alias}@southslopenano.com">{alias}@southslopenano.com</a>'
            + ' if the button doesn\'t open your mail app.</p>'
        )
        if cta_button_close in text:
            text = text.replace(cta_button_close, new_block)
            changes.append('added fallback line')

    if changes:
        path.write_text(text, encoding='utf-8')
    return bool(changes), changes


def main():
    report = []
    for v in VARIANTS:
        path = DOCS / f'{v}.html'
        if not path.exists():
            report.append((v, False, ['MISSING FILE']))
            continue
        ok, changes = patch(path, v)
        report.append((v, ok, changes))

    for v, ok, changes in report:
        print(f'  {v:<12} {"OK" if ok else "noop"}  {changes}')

if __name__ == '__main__':
    main()
