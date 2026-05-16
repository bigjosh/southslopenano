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

## 2. Conversion gap on Meta — 38 LPVs, 0 mailto sends

**Question:** Meta is delivering at $0.11/Landing Page View (good cost) but converting at 0%. 38 people loaded a landing page; zero clicked the mailto and sent an email. Two proposed fixes (need your sign-off on edits since they publish under your domain):

**A. Soften the mailto friction.** Drop the prefilled body `"I plan to upload: "` — current text implies you need a fully-formed idea before clicking, which is enough to scare off a chunk of mobile users whose default email client just opened a blank-feeling reply. Default the body to a brief friendly nudge or leave it empty.

**B. Add a visible plaintext fallback under the CTA button.** Some mobile browsers don't have a mailto handler configured (especially Android Chrome where Gmail is logged out, or browsers in incognito). A line like *"Or email us directly at sapphire@southslopenano.com"* under the button catches those users.

Both edits are cross-cutting across all 8 variant landing pages — should I make the change? Either A, B, both, or neither?

**Status:** OPEN — the binding constraint on Phase 1 isn't ad spend, it's this conversion rate. Bumping Meta budget without fixing it just burns money.

---

## 3. Moderation policy ratification

**Question:** Confirm the moderation default — bounce porn, hate symbols, third-party commercial logos, doxxing of third parties, and clearly AI-generated work without human modification. Anything to add or remove? Who reviews edge cases — Josh, or is there delegation?

**Why it matters:** Once uploads come in volume, we need a working policy. The `claim.html` honest-notes section already promises "we review every upload."

**Status:** Open, but lower priority — not blocking until first wave of uploads.
