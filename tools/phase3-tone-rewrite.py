"""Phase 3 tone rewrite — reorient all 8 variant pages around the
'we're curating cool stuff for an unusual physical artifact' framing.

Structural changes:
  - Move 'Already on the disk' gallery ABOVE the upload form
  - Rename heading 'Upload a tile.' -> 'Submit a tile.'
  - New intro copy: invitation tone + format spec + link to /how-to.html
  - Replace 'What's actually happening' + 'Honest notes' tail with two
    new sections: 'What this actually is' (the artifact reveal) and
    'Want to own one?' (the soft sell with the $150 Stripe link).
  - Moderation note moves to fine-print under the form (where it
    actually matters at decision time).

Region replaced: from `<h1>Mosaic</h1>` through (not including)
`<footer>` -- the entire main content. The form HTML is reproduced
verbatim per page with the right `source` alias baked in, so the
form-handler JS keeps finding all its DOM hooks.

CSS, scripts, footer, head, StatCounter snippet, click-tracker, and
phase2 form-handler JS are all left untouched.

Idempotent — re-running detects the new structure (presence of
'<h2>Submit a tile.</h2>') and replaces it the same way.
"""

import re
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / 'docs'

PAGES = [
    'mosaic.html',
    'sapphire.html', 'pixel.html', 'tile.html', 'lockin.html',
    'foundry.html', 'etch.html', 'jb-mosaic.html',
]

STRIPE_URL = "https://buy.stripe.com/6oU6oG1Wu0dX3zs0BD7ok08"
HOWTO_URL = "/how-to.html"
VIEWER_URL = "https://mosaic.southslopenano.com"


def body_block(alias: str) -> str:
    return f"""<h1>Mosaic</h1>
    <p class="tagline">A 29mm sapphire disk, etched in gold by semiconductor lithography. 1,124 contributors, one disk.</p>

    <img src="/disk-photo.jpg" alt="The Mosaic disk &mdash; a 29mm sapphire wafer with gold-etched contents, held in a gloved hand" class="hero-img">

    <p class="counter">
      <span class="filled" id="filled-count">&hellip;</span> of 1,124 tiles filled.
      <span id="remaining-count">&hellip;</span> remain.
    </p>

    <p class="deadline-line">
      File locks on <span class="deadline">May 24, 2026</span>. After that the disk goes to fabrication.
    </p>

    <h2>Already on the disk</h2>
    <p class="fine center">Some of what people have already sent in.</p>
    <div id="tile-gallery" class="tile-grid"></div>
    <p class="center"><button id="more-tiles" type="button" class="btn-link">Show 9 more &rarr;</button></p>

    <h2>Submit a tile.</h2>
    <p>We're curating 1,124 little pictures for a sapphire disk we're fabricating this May. Looking for cool stuff &mdash; pixel art, sketches, drawings, photos, anything that reads as 500&times;500 black-and-white.</p>

    <p>Tiles are <strong>500&times;500 pixels, 1-bit</strong> (pure black or white, no gray). Drop any image and we'll convert it for you, or <a href="{HOWTO_URL}">prepare your own</a> if you want full control.</p>

    <form id="claim-form" class="claim-form" enctype="multipart/form-data">
      <input type="hidden" name="source" value="{alias}">

      <p id="dropzone-label" class="fine center" style="margin: 0 0 10px;">Drop an image here, or click to pick one.</p>
      <label class="dropzone" id="dropzone">
        <input type="file" accept="image/*" hidden id="file-input">
        <span class="dropzone-plus" aria-hidden="true">+</span>
        <canvas id="preview-canvas" width="500" height="500" hidden></canvas>
      </label>

      <div class="preview-controls" id="preview-controls" hidden>
        <button type="button" id="btn-invert" class="btn-secondary">Invert colors</button>
        <button type="button" id="btn-redo" class="btn-secondary">Try a different image</button>
      </div>

      <label class="email-row">
        <span class="email-label">Your email <span class="muted">(optional &mdash; no spam, just a couple of updates like where to find your image on the fabricated disk)</span></span>
        <input type="email" name="email" placeholder="you@example.com" autocomplete="email">
      </label>

      <p class="cta-wrap">
        <button type="submit" class="cta-button" id="submit-btn" disabled>Submit my tile</button>
      </p>
      <p class="fine center" id="claim-status" aria-live="polite"></p>
    </form>

    <p class="fine">Be cool and creative &mdash; anything we wouldn't want next to our own image gets bounced.</p>

    <hr class="divider">

    <h2>What this actually is</h2>
    <p>Semiconductor lithography &mdash; the same process that makes microchips &mdash; but instead of circuits, we're etching pictures. The result is a 29mm sapphire wafer with up to 1,124 little tiles, each one pure gold on the surface. The tiles are about half a millimeter wide &mdash; too small to read with the naked eye, but big in aggregate.</p>

    <p>The disk doesn't need electricity, software, or an internet connection to be read &mdash; just a microscope. Sapphire and gold both age extremely well; we expect the disks to be around for the next 10,000 years.</p>

    <p>The full-resolution contents also live permanently at <a href="{VIEWER_URL}" target="_blank" rel="noopener">mosaic.southslopenano.com</a>, but the disk is the canonical record. It's a small, permanent snapshot of what people online were drawing in May 2026.</p>

    <h2>Want to own one?</h2>
    <p>Each contributor can buy a finished disk for $150. Your tile is on it, along with everyone else's &mdash; every disk is identical. We're fabricating a small batch; once they're gone they're gone. It's the closest most people will ever get to seeing semiconductor lithography up close.</p>

    <p class="cta-wrap"><a class="cta-button" href="{STRIPE_URL}" target="_blank" rel="noopener">Buy a disk &mdash; $150</a></p>

    """


# The region runs from <h1>Mosaic</h1> through (and not including) the
# opening <footer> tag. Match non-greedy.
BODY_REGION_RE = re.compile(
    r'<h1>Mosaic</h1>[\s\S]*?(?=<footer>)',
    re.MULTILINE,
)


# Also need to update the success-message inside the form-handler JS,
# since the new copy says "submission" instead of "tile" and we want
# consistent voice.
OLD_SUCCESS = (
    "<p class='success'>Got it &mdash; your tile is in the queue. "
    "We'll review it before file-lock on May 24. Thank you.</p>"
)
NEW_SUCCESS = (
    "<p class='success'>Got it &mdash; your submission is in the queue. "
    "We'll review it before file-lock on May 24 and let you know if you "
    "left an email. Thank you for contributing.</p>"
)


def patch(path: Path, alias: str) -> bool:
    text = path.read_text(encoding='utf-8')
    original = text

    if not BODY_REGION_RE.search(text):
        return False  # signal error to caller
    text = BODY_REGION_RE.sub(body_block(alias), text, count=1)

    if OLD_SUCCESS in text:
        text = text.replace(OLD_SUCCESS, NEW_SUCCESS)

    if text == original:
        return None  # unchanged
    path.write_text(text, encoding='utf-8')
    return True


def main():
    for name in PAGES:
        path = DOCS / name
        if not path.exists():
            print(f'  {name:<16} MISSING')
            continue
        alias = name.replace('.html', '')
        result = patch(path, alias)
        if result is False:
            print(f'  {name:<16} ERROR - body region not found')
        elif result is None:
            print(f'  {name:<16} unchanged')
        else:
            print(f'  {name:<16} OK')


if __name__ == '__main__':
    main()
