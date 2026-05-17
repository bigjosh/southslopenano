# Phase 3 ad angles — "submit cool stuff" voice

Three angles, drafted for both Reddit and Meta. Voice rewrite of the
old `copy/ads/reddit/angle-{1,2,3,4}-*.md` and
`copy/ads/meta/variants-for-phase2.md` — those are now superseded.

Tone direction (Josh, 2026-05-17):
- We're curating cool stuff for a physical artifact.
- Drop "free" verbiage entirely.
- "Submit" not "upload" or "claim" — implies editorial selection.
- The disk is a serious physical object that'll last 10,000 years, not
  a freemium tile-claim.
- The $150 ask is "want to own one of these objects?" not "buy a souvenir
  of your tile."

All three angles point at the variant landing pages; the
`?source=` URL param overrides the per-page hidden field so Josh can
tag specific ad URLs without making new pages.

Destination URLs use existing variants for attribution: pixel-art →
`/pixel.html`, scarcity/HN → `/sapphire.html`, general invitation →
`/tile.html`. Per-platform attribution lands in StatCounter Exit Links
plus the Worker's KV-stored `source` field.

---

## Angle A — "Got something cool?" (general invitation)

The most universal angle. Lead with the invitation; let the
permanence/material details earn their place on the landing page.

### Reddit

**Title:** We're etching 1,124 little pictures into gold on a sapphire disk this May. Got something cool to send in?

**Image:** Disk photo (`/disk-photo.jpg`).

**Link card subtitle:** A real semiconductor-lithography artifact. Submissions close May 24. We review every one.

**Destination URL:** `https://southslopenano.com/tile.html`

**Target subs:** r/somethingimade, r/InternetIsBeautiful, r/Aesthetic, r/woahdude

**Notes:** Plainspoken, no jargon. Curiosity hook. Works because most
people skimming Reddit have *some* cool image in mind already.

### Meta

**Primary text:** We're etching 1,124 little pictures into gold on a 29mm sapphire disk this May. Got something cool to send in? Submissions close May 24.

**Headline:** Send us something for the disk

**Description:** 29mm sapphire, etched in gold

**CTA:** Sign up

**Destination URL:** `https://southslopenano.com/tile.html?source=tile`

---

## Angle B — "Your pixel art, in literal gold" (for pixel-art communities)

Speak directly to communities that already think in 1-bit / small
canvases / permanence.

### Reddit

**Title:** Send us your pixel art. We'll etch it in gold on a sapphire disk that'll outlast everyone reading this.

**Image:** Disk photo with a callout to a single tile, magnified.

**Link card subtitle:** 1,124 contributors. One disk. 500×500 1-bit tiles. Submissions open until May 24.

**Destination URL:** `https://southslopenano.com/pixel.html`

**Target subs:** r/PixelArt, r/aseprite, r/pico8, r/IndieDev

**Notes:** "Outlast everyone reading this" is the line that should
stick. Pixel art people already work in 1-bit; the medium fit is
obvious to them.

### Meta

**Primary text:** Send us your pixel art. We'll etch it in gold on a real 29mm sapphire disk. 1-bit native, 500×500 — your work, in literal gold.

**Headline:** Pixel art, in literal gold

**Description:** Sapphire-and-gold disk, May 24 deadline

**CTA:** Sign up

**Destination URL:** `https://southslopenano.com/pixel.html?source=pixel`

---

## Angle C — "A permanent record of what the internet was drawing" (HN / one-of-N / design crowd)

Frame as cultural curation. For audiences that care about archives,
artifacts, and the post-NFT-crash conversation about permanence.

### Reddit

**Title:** We're curating 1,124 images for a permanent physical archive of what the internet was drawing in May 2026 — etched in gold on a sapphire disk.

**Image:** Disk photo at full clarity (the gold-on-sapphire surface).

**Link card subtitle:** Semiconductor lithography. 10,000-year lifespan. No software, no servers — just a microscope. Submit something cool.

**Destination URL:** `https://southslopenano.com/sapphire.html`

**Target subs:** r/InternetIsBeautiful, r/SideProject, r/Aesthetic, r/Art, r/somethingimade

**Notes:** Heavier on the artifact/archive language. Aimed at the
"one-of-N collectors" audience from CLAUDE.md (Are.na, post-NFT
tasteful crowd, HN-style design readers). Pairs naturally with a
Show HN post written in the same voice if Josh wants to do that
organic in parallel.

### Meta

**Primary text:** A permanent physical archive of what the internet was drawing in May 2026 — etched in gold on a sapphire disk that won't need the internet to be read in the year 12,026. 1,124 contributors. Submit something cool.

**Headline:** A 10,000-year sapphire archive

**Description:** Semiconductor lithography. Submissions close May 24.

**CTA:** Sign up

**Destination URL:** `https://southslopenano.com/sapphire.html?source=sapphire`

---

## Deployment notes

- **Run one angle at a time per ad set** so we can read which angle/copy
  is doing the work. Avoid auction-against-self.
- **Start with Angle A** (general invitation) — broadest top-of-funnel,
  cheapest to validate the new voice before specializing.
- **Add Angle B** once we have a baseline. Pixel-art audiences have the
  strongest natural fit and should produce the best click-to-submission
  rate.
- **Hold Angle C** for HN organic posting first (no paid spend). If the
  Show HN lands well, then promote via paid in the same voice.
- **Image:** all three angles can reuse `/disk-photo.jpg` for v1. Custom
  imagery (e.g. magnified single tile, full-disk crop) is a v2 ask.
- **Old creative files** at `copy/ads/reddit/angle-{1..4}-*.md` and
  `copy/ads/meta/variants-for-phase2.md` are superseded but kept for
  retrospective.
