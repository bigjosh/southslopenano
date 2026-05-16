# Meta ad variant drafts — Phase 2 deployment candidates

Phase 1 Meta data (through 2026-05-15 evening):

- **Scarcity ad** ("Scarcity - 1124 cap - Meta") → /sapphire.html → sapphire@. ~23-25 LPVs at $0.12/LPV, 0 conversions (pre-conversion-fix).
- **r/place ad** ("A1V2 - like r/place - Meta") → /pixel.html → pixel@. ~17-22 LPVs at $0.11-0.13/LPV, 0 conversions (pre-fix).

Both delivering. Both spending well under-budget (Meta throttling). Daily budgets bumped to $50/ad-set on 2026-05-15.

If after 24-48h with the new conversion-fix landing pages we still see zero or near-zero mailto sends, the ad copy is the next variable to test. Drafts below are deployable then.

---

## Variant M-D: "free upload" lead

Same hypothesis as Reddit Angle 4 — drop the implicit $150 anxiety from the ad. Conversion happens after upload on claim.html.

**Primary text (Meta "Primary text" field, 125 chars hard limit shows on most placements):**
> Upload a 500×500 pixel image. We etch it in gold on a real sapphire disk. Free.

**Headline (40 chars typical):**
> Free pixel art on a sapphire disk

**Description (optional, 30 chars typical):**
> File locks May 24, 2026

**CTA button:** Learn more

**Destination URL:** `https://southslopenano.com/tile.html`

**Why:** Lower cognitive friction in the ad. "Free" is a 4-character magnet. The disk material is the proof-of-real underneath.

---

## Variant M-E: simple counter

Use the live tile count as the hook. The landing page already shows it; the ad echoes it.

**Primary text:**
> 243 of 1,124 tiles claimed. Each tile is a 500×500 pixel image etched in gold on a 29mm sapphire disk. Upload yours — free.

**Headline:**
> 881 sapphire tiles remain

**Description:**
> One physical run, May 24 file-lock

**CTA button:** Sign up

**Destination URL:** `https://southslopenano.com/lockin.html`

**Why:** Specific numbers. "243" tells the reader other people are doing this. "881 remain" gives a clear opportunity-size. Numbers will need refreshing as the count moves (or rotate creative weekly).

---

## Variant M-F: anti-NFT framing

Targets the post-NFT-crash audience that values permanence but is jaded about "digital collectibles."

**Primary text:**
> Not a JPEG. Not an NFT. A real 29mm sapphire disk with your 500×500 pixel art etched in gold using semiconductor lithography. Free to upload.

**Headline:**
> Real lithography, not a JPEG

**Description:**
> 1,124 contributors, one physical disk

**CTA button:** Sign up

**Destination URL:** `https://southslopenano.com/foundry.html`

**Why:** Specifically rejects the comparison the audience is going to make anyway, on stronger ground. "Real lithography" is the technical credibility marker. Targets the "one of N collectors" ring.

---

## Deployment plan

When triggering: launch one variant at a time (Meta penalizes ad-set sibling competition). Start with M-D (free-lead) at $50/day mirroring current ad sets. After 24h, evaluate. If M-D outperforms, rotate the current Scarcity-1124 / A1V2 ads out. If it doesn't, try M-E, then M-F.

All variants reuse the existing disk photo (`/disk-photo.jpg`) — no new asset production needed.
