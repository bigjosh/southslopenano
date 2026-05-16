# DECISIONS_QUEUE.md

Yes/no items waiting on Josh. Keep this short — if it grows past 5 items, work is stalled.

Format: one item per section. Move resolved items into `STATE.md`'s decision log and delete from here.

---

## 1. Reddit billing — fund the campaigns

**Question:** Reddit Ads is showing "Not delivering / Campaign not funded" on both Scarcity and r/place. The billing page shows Mastercard 8144, $0 balance, $1.50 threshold, last transactions Nov 2025, and **Tax Information section completely blank** (no Tax ID, no business address). $27 was spent before delivery stopped.

**Two likely causes, both your action:**
- (a) Tax Information must be filled — Reddit blocks delivery for US advertisers above a low spend threshold without it.
- (b) Card may have declined or been deauthorized; verify Mastercard 8144 is current and active.

**What I need:** confirmation once tax info is in + card is verified, so I can re-check delivery status next cycle.

**Status:** OPEN — primary blocker on Reddit channel. Phase 1 has ~36 hours left; every hour Reddit is dark is lost spend headroom.

---

## 2. Conversion gap on Meta — fix shipped, measuring

**Original problem:** Meta delivering at $0.11/Landing Page View but 0% mailto conversion. Acted autonomously on goal directive's "be bold" mandate:

- **Edit A shipped:** rephrased "in the body, briefly mention what you plan to upload" → "tell us about your idea if you want — we love seeing what people are planning". Drops the implicit demand for a fully-formed pitch.
- **Edit B shipped:** added a plaintext fallback line under the CTA: *"Or write directly to X@southslopenano.com if the button doesn't open your mail app."*
- Also dropped the `body=I%20plan%20to%20upload%3A%20` mailto prefill so the email opens with a blank body, less pressure to compose.

All three changes applied across all 8 variants (sapphire/pixel/tile/lockin/foundry/etch/jb-mosaic/mosaic). Pushed to GH Pages, verified live. Holler if you'd rather have rolled back any of these.

**Status:** Shipped. Now measuring — will report effect on conversion rate over next 12–24 hours.

---

## 3. Ad-copy refresh — Meta headlines lack a CTA

**Observation (2026-05-15 mid-cycle check):** Inspected the live Meta ad copy directly. Both ads share the same dry primary text body ("A 29mm sapphire disk, etched in gold by semiconductor lithography. 1,124 tiles. File-locks May 24, 2026."). Headlines:

- **r/place ad:** *"Like r/place, but it ships to your door."* — catchy, but "ships to your door" implies free shipping when in fact the disk is $150. Mild expectation mismatch on click.
- **Scarcity ad:** *"1,124 tiles on a sapphire disk"* — pure descriptive, no CTA, doesn't tell the reader what action is wanted.

**Why this matters:** The reader has no CTA-shaped thought when they land on the page. The conversion fix shipped today clarifies the on-page CTA but the ad-side doesn't prime them to look for one.

**Proposed (drafts already in `copy/ads/meta/variants-for-phase2.md`):**
- M-D "free-lead": primary text leads with *"Upload a 500×500 pixel image. We etch it in gold on a real sapphire disk. Free."* Headline: *"Free pixel art on a sapphire disk"*.
- Hold off rotating until conversion-fix data lands (24-48h) to keep variables separable.

**Status:** Just-noted, not blocking. Phase 2 candidate. Surface when reviewing Phase 1 results.

---

## 4. Moderation policy ratification

**Question:** Confirm the moderation default — bounce porn, hate symbols, third-party commercial logos, doxxing of third parties, and clearly AI-generated work without human modification. Anything to add or remove? Who reviews edge cases — Josh, or is there delegation?

**Why it matters:** Once uploads come in volume, we need a working policy. The `claim.html` honest-notes section already promises "we review every upload."

**Status:** Open, but lower priority — not blocking until first wave of uploads.
