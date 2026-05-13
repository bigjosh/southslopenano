# DECISIONS_QUEUE.md

Yes/no items waiting on Josh. Keep this short — if it grows past 5 items, work is stalled.

Format: one item per section. Move resolved items into `STATE.md`'s decision log and delete from here.

---

## 1. Email-collection submission endpoint

**Question:** What submits the landing-page email form? The form currently has `action="[EMAIL_ENDPOINT]"` as a placeholder. Options:

- A third-party form service (Formspark, Formspree, Tally, Netlify Forms, etc.) — fastest to set up, free tiers cover this campaign's volume. Submissions arrive in Josh's inbox.
- A custom endpoint on the existing upload server (`mosaic.southslopenano.com`) — violates CLAUDE.md's "don't touch the backend" unless Josh waives it.
- A `mailto:` link — opens user's email client. Zero infrastructure, but heavy friction on mobile and for users without configured email clients.

**Why it matters:** Blocks running paid ads. The form is non-functional until the action attribute points at something real. Conversion tracking also depends on the choice — some services give submission counts; for others we'd need a thank-you page that fires a Reddit pixel.

**Status:** Open. Highest priority — blocks the entire campaign launch.

---

## 2. Physical disk photography

**Question:** Any real photo of the physical disk (or a previous run's disk) available? Even bad lighting, on a fingertip, next to a coin for scale.

**Why it matters:** Real-object photos with scale context dramatically outperform renders. The landing page currently uses `disk.png` from the upload server, which appears to be a render. Same image is suggested for several ad creatives.

**Status:** Open. Workable without, but a real photo would significantly improve the landing page and ad creative.

---

## 3. Moderation policy ratification

**Question:** Confirm the moderation default — bounce porn, hate symbols, third-party commercial logos, doxxing of third parties, and clearly AI-generated work without human modification. Anything to add or remove? Who reviews edge cases — Josh, or is there delegation?

**Why it matters:** Once uploads come in volume, we need a working policy. The `claim.html` honest-notes section already promises "we review every upload."

**Status:** Open, but lower priority — not blocking until first wave of uploads.
