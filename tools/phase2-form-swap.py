"""Phase 2 pivot: replace the mailto CTA on the 8 variant landing pages
with an in-page upload form (drop-zone + canvas preview with Floyd-
Steinberg dithering to 500x500 1-bit) and add a 'Already on the disk'
social-proof gallery.

Three insertion points per file:
  1. CSS block — extra rules appended into the existing <style>.
     Marker: /* phase2 form styles */
  2. Body content — replaces from <h2>Claim a tile.</h2> through the
     fine-print blurb that precedes <hr class="divider">. Marker:
     <form id="claim-form"> appears only after the swap.
  3. JS block — form handler, dithering, submit. Inserted before
     </body>. Marker: // phase2 form handler

The Worker URL is left as `__WORKER_URL__` until Josh deploys the
Worker and tells us the actual hostname; a tiny separate script will
do the final substitution.

Idempotent — re-running replaces existing markers cleanly.
"""

import re
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / 'docs'

PAGES = [
    'mosaic.html',
    'sapphire.html', 'pixel.html', 'tile.html', 'lockin.html',
    'foundry.html', 'etch.html', 'jb-mosaic.html',
]

# Stem -> alias for the hidden `source` form field.
def alias_for(name): return name.replace('.html', '')


# ---------- 1. CSS block ----------
CSS_MARKER = '/* phase2 form styles */'
CSS_BLOCK = """
/* phase2 form styles */
.claim-form {
  background: #141414;
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 20px;
  margin: 8px 0 20px;
}
.dropzone {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-height: 280px;
  background: #0a0a0a;
  border: 2px dashed var(--border);
  border-radius: 6px;
  cursor: pointer;
  text-align: center;
  padding: 16px;
  transition: border-color .15s, background .15s;
}
.dropzone.over { border-color: var(--accent); background: #122; }
.dropzone:hover { border-color: var(--accent); }
#dropzone-label { color: var(--muted); font-size: 1rem; }
#preview-canvas {
  display: block;
  width: 100%;
  max-width: 300px;
  height: auto;
  image-rendering: pixelated;
  background: #fff;
  border-radius: 4px;
}
.preview-controls {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin: 16px 0 4px;
  flex-wrap: wrap;
}
.btn-secondary {
  background: transparent;
  color: var(--accent);
  border: 1px solid var(--accent);
  padding: 10px 18px;
  border-radius: 4px;
  font-family: inherit;
  font-size: 1rem;
  cursor: pointer;
}
.btn-secondary:hover { background: rgba(0,255,255,0.08); }
.email-row {
  display: block;
  margin: 20px 0 8px;
}
.email-row .email-label {
  display: block;
  margin-bottom: 8px;
  font-size: 1rem;
  color: var(--soft);
}
.email-row .muted { color: var(--muted); font-weight: 400; }
.email-row input[type="email"] {
  width: 100%;
  padding: 12px 14px;
  background: #0a0a0a;
  color: var(--fg);
  border: 1px solid var(--border);
  border-radius: 4px;
  font-family: inherit;
  font-size: 1rem;
}
.email-row input[type="email"]:focus { border-color: var(--accent); outline: none; }
.cta-button:disabled { opacity: 0.45; cursor: not-allowed; }
.success {
  color: var(--accent);
  font-size: 1.125rem;
  text-align: center;
  padding: 24px 8px;
}
.tile-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  margin: 12px 0 12px;
}
.tile-grid img {
  width: 100%;
  aspect-ratio: 1 / 1;
  display: block;
  image-rendering: pixelated;
  background: #222;
  border-radius: 3px;
  border: 1px solid var(--border);
}
.btn-link {
  background: none;
  border: none;
  color: var(--accent);
  font-family: inherit;
  font-size: 1rem;
  cursor: pointer;
  padding: 8px;
}
.btn-link:hover { opacity: 0.85; }
"""

CSS_REGION_RE = re.compile(
    r'\n*/\* phase2 form styles \*/[\s\S]*?(?=\n  </style>|\n</style>)',
    re.MULTILINE,
)


def patch_css(text: str) -> str:
    # Drop any prior block.
    text = CSS_REGION_RE.sub('', text)
    # Insert before </style>.
    if '</style>' not in text:
        raise RuntimeError('no </style> found')
    return text.replace('</style>', CSS_BLOCK + '\n  </style>', 1)


# ---------- 2. Body content ----------
def body_block(alias: str) -> str:
    return f"""<h2>Claim a tile.</h2>
    <p>Drop or pick any image. We'll convert it to 500×500 black-and-white right here in your browser, show you the preview, and etch <em>that exact image</em> on the disk in gold. Free.</p>

    <form id="claim-form" class="claim-form" enctype="multipart/form-data">
      <input type="hidden" name="source" value="{alias}">

      <label class="dropzone" id="dropzone">
        <input type="file" accept="image/*" hidden id="file-input">
        <span id="dropzone-label">Drop an image here, or click to pick one</span>
        <canvas id="preview-canvas" width="500" height="500" hidden></canvas>
      </label>

      <div class="preview-controls" id="preview-controls" hidden>
        <button type="button" id="btn-invert" class="btn-secondary">Invert colors</button>
        <button type="button" id="btn-redo" class="btn-secondary">Try a different image</button>
      </div>

      <label class="email-row">
        <span class="email-label">Your email <span class="muted">(optional &mdash; we'll send a confirmation)</span></span>
        <input type="email" name="email" placeholder="you@example.com" autocomplete="email">
      </label>

      <p class="cta-wrap">
        <button type="submit" class="cta-button" id="submit-btn" disabled>Add my tile</button>
      </p>
      <p class="fine center" id="claim-status" aria-live="polite"></p>
    </form>

    <p class="fine">Want the physical disk after fabrication? Each contributor can buy one for $150 &mdash; but your image goes on the disk either way. Every buyer gets an identical disk with your image and everyone else's.</p>

    <h2>Already on the disk</h2>
    <p class="fine center">A few of the tiles people have added so far.</p>
    <div id="tile-gallery" class="tile-grid"></div>
    <p class="center"><button id="more-tiles" type="button" class="btn-link">Show 9 more &rarr;</button></p>

    """


# Match from the "Claim a tile" h2 through whatever fills the gap up
# to the divider <hr>. Captures both the original mailto layout AND
# any prior form layout (for re-run idempotency).
BODY_REGION_RE = re.compile(
    r'<h2>Claim a tile\.</h2>[\s\S]*?(?=<hr class="divider">)',
    re.MULTILINE,
)


def patch_body(text: str, alias: str) -> str:
    if not BODY_REGION_RE.search(text):
        raise RuntimeError('Claim-a-tile section not found')
    return BODY_REGION_RE.sub(body_block(alias), text, count=1)


# ---------- 3. JS block ----------
JS_MARKER = '// phase2 form handler'
JS_REGION_RE = re.compile(
    r'\n*<script>\s*\n//\s*phase2 form handler[\s\S]*?</script>\n*',
    re.MULTILINE,
)
JS_BLOCK = """
<script>
// phase2 form handler — client-side 500x500 1-bit dithering + submit
(function () {
  const WORKER = "__WORKER_URL__";
  const form = document.getElementById("claim-form");
  if (!form) return;
  const fileInput = document.getElementById("file-input");
  const dropzone = document.getElementById("dropzone");
  const canvas = document.getElementById("preview-canvas");
  const ctx = canvas.getContext("2d", { willReadFrequently: true });
  const dzLabel = document.getElementById("dropzone-label");
  const controls = document.getElementById("preview-controls");
  const status = document.getElementById("claim-status");
  const btn = document.getElementById("submit-btn");
  let inverted = false;
  let lastSource = null;

  async function loadAndConvert(file) {
    try {
      lastSource = await createImageBitmap(file);
      inverted = false;
      render();
    } catch (e) {
      status.textContent = "Couldn't read that image. Try a different file.";
    }
  }

  function render() {
    if (!lastSource) return;
    const W = 500, H = 500;
    const sw = lastSource.width, sh = lastSource.height;
    const side = Math.min(sw, sh);
    const sx = (sw - side) / 2, sy = (sh - side) / 2;
    ctx.drawImage(lastSource, sx, sy, side, side, 0, 0, W, H);
    const img = ctx.getImageData(0, 0, W, H);
    const d = img.data;
    const lum = new Float32Array(W * H);
    for (let i = 0, p = 0; i < d.length; i += 4, p++) {
      lum[p] = 0.299 * d[i] + 0.587 * d[i + 1] + 0.114 * d[i + 2];
    }
    for (let y = 0; y < H; y++) {
      for (let x = 0; x < W; x++) {
        const p = y * W + x;
        const old = lum[p];
        const target = inverted ? (old < 128 ? 255 : 0) : (old < 128 ? 0 : 255);
        const err = old - target;
        lum[p] = target;
        if (x + 1 < W)        lum[p + 1]     += err * 7 / 16;
        if (y + 1 < H) {
          if (x > 0)          lum[p + W - 1] += err * 3 / 16;
                              lum[p + W]     += err * 5 / 16;
          if (x + 1 < W)      lum[p + W + 1] += err * 1 / 16;
        }
      }
    }
    for (let i = 0, p = 0; i < d.length; i += 4, p++) {
      const v = lum[p] >= 128 ? 255 : 0;
      d[i] = d[i + 1] = d[i + 2] = v; d[i + 3] = 255;
    }
    ctx.putImageData(img, 0, 0);
    canvas.hidden = false;
    dzLabel.hidden = true;
    controls.hidden = false;
    btn.disabled = false;
    status.textContent = "";
  }

  fileInput.addEventListener("change", e => {
    const f = e.target.files && e.target.files[0];
    if (f) loadAndConvert(f);
  });

  ["dragenter","dragover"].forEach(ev =>
    dropzone.addEventListener(ev, e => { e.preventDefault(); dropzone.classList.add("over"); }));
  ["dragleave","drop"].forEach(ev =>
    dropzone.addEventListener(ev, e => { e.preventDefault(); dropzone.classList.remove("over"); }));
  dropzone.addEventListener("drop", e => {
    const f = e.dataTransfer.files && e.dataTransfer.files[0];
    if (f) loadAndConvert(f);
  });

  document.getElementById("btn-invert").addEventListener("click", () => {
    inverted = !inverted;
    render();
  });
  document.getElementById("btn-redo").addEventListener("click", () => {
    lastSource = null; inverted = false;
    canvas.hidden = true; controls.hidden = true; dzLabel.hidden = false;
    fileInput.value = ""; btn.disabled = true;
    status.textContent = "";
    fileInput.click();
  });

  const sourceField = form.querySelector("input[name='source']");
  const source = sourceField ? sourceField.value : "direct";

  form.addEventListener("submit", e => {
    e.preventDefault();
    if (!lastSource) { status.textContent = "Pick an image first."; return; }
    btn.disabled = true;
    const origText = btn.textContent;
    btn.textContent = "Sending…";
    status.textContent = "";
    canvas.toBlob(async blob => {
      const fd = new FormData();
      fd.set("image", blob, "tile.png");
      fd.set("email", form.email.value || "");
      fd.set("source", source);
      try {
        const r = await fetch(WORKER, { method: "POST", body: fd });
        const data = await r.json().catch(() => ({}));
        if (r.status === 429) {
          status.textContent = "You've sent a few already from this network. Try again in ~10 minutes.";
        } else if (!r.ok || !data.ok) {
          status.textContent = "Something went wrong (" + (data.error || r.status) + "). Try again in a minute.";
        } else {
          form.innerHTML = "<p class='success'>Got it. Your tile is in the queue. Thank you.</p>";
          if (window.trackEvent) window.trackEvent("upload:success:" + source);
          return;
        }
      } catch (err) {
        status.textContent = "Network error. Try again.";
      }
      btn.disabled = false;
      btn.textContent = origText;
    }, "image/png");
  });
})();
</script>

<script>
// phase2 tile gallery — 9 random thumbs from /tiles/manifest.json
(function () {
  const grid = document.getElementById("tile-gallery");
  const moreBtn = document.getElementById("more-tiles");
  if (!grid) return;
  fetch("/tiles/manifest.json").then(r => r.json()).then(names => {
    function render() {
      grid.innerHTML = "";
      const picks = [...names].sort(() => Math.random() - 0.5).slice(0, 9);
      for (const n of picks) {
        const img = document.createElement("img");
        img.src = "/tiles/" + n;
        img.loading = "lazy";
        img.alt = "a contributor's tile";
        grid.appendChild(img);
      }
    }
    render();
    if (moreBtn) moreBtn.addEventListener("click", render);
  }).catch(() => {
    if (moreBtn) moreBtn.hidden = true;
  });
})();
</script>
"""


def patch_js(text: str) -> str:
    text = JS_REGION_RE.sub('', text)
    if '</body>' not in text:
        raise RuntimeError('no </body> found')
    # Insert at the top of the </body> trailing scripts area.
    # Place BEFORE the existing StatCounter snippet so the form handler
    # loads early, but it doesn't matter much since everything is on
    # DOMContentLoaded or click events.
    return text.replace('</body>', JS_BLOCK + '\n</body>', 1)


def main():
    for name in PAGES:
        path = DOCS / name
        if not path.exists():
            print(f'  {name:<16} MISSING')
            continue
        text = path.read_text(encoding='utf-8')
        original = text
        try:
            text = patch_css(text)
            text = patch_body(text, alias_for(name))
            text = patch_js(text)
        except RuntimeError as e:
            print(f'  {name:<16} ERROR {e}')
            continue
        if text == original:
            print(f'  {name:<16} unchanged')
            continue
        path.write_text(text, encoding='utf-8')
        print(f'  {name:<16} OK')


if __name__ == '__main__':
    main()
