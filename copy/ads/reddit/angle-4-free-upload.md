# Angle 4 — upload is free, lead with that

The previous three angles all implicitly carried the $150 disk as a price barrier readers had to climb over. This angle inverts: lead with "free upload, image lives on a real semiconductor-etched disk forever," skip the price entirely until the conversion surface. Per the goal, free uploads are still valuable (marketing surface area, more tiles filled = better disk). The $150 sell happens *after* upload on `claim.html`, not in the ad.

**Target subreddits:**
- r/PixelArt (Angle 1 overlap — but with much lower cognitive load on the ad itself)
- r/aseprite
- r/IndieDev / r/IndieGaming
- r/somethingimade
- r/InternetIsBeautiful
- r/SideProject

**Image direction:**
- Variant A: just the disk photo, with a single overlaid line of text.
- Variant B: a 500×500 pixel-art demo (whatever Josh has on hand or we mock) with a small inline arrow → tiny disk image. The pixel-art-to-disk transformation visual.

**Why this might outperform:**
- Removes purchase-anxiety from the ad. Reader thinks "huh, free, why not?" rather than "do I want to spend $150 on this?"
- Conversion fix shipped 2026-05-15 already lowered the mailto friction; this ad-side lowers the cognitive friction.
- Matches the funnel reality: ~80% of inbound emails are unlikely to convert to $150 disk buyers anyway; we want them anyway because their images make the disk better.

---

## Variant A — minimal

**Title:** Upload a 500×500 image. We etch it in gold on a sapphire disk. Free.

**Image:** Disk photo, no overlaid text.

**Link card subtitle:** Real semiconductor lithography. 1,124 contributors on one disk. File locks May 24.

**Destination URL:** `https://southslopenano.com/tile.html` (recipient: `tile@`)

**Notes:** Three short sentences. Each is a fact. Resists the urge to add adjectives.

---

## Variant B — emphasize the medium

**Title:** Your pixel art, etched in gold on a 29mm sapphire disk. Free to upload.

**Image:** Disk photo with a callout pointing to a single tile, magnified.

**Link card subtitle:** 1,124 tiles. Every contributor's image appears on every disk. After May 24, the file locks.

**Destination URL:** `https://southslopenano.com/etch.html` (recipient: `etch@`)

**Notes:** "Etched in gold" is the line. Concrete material, concrete process. Distinguishes from generic NFT/crypto pitches.

---

## Variant C — for r/IndieDev / r/aseprite

**Title:** Your sprite, permanently on a sapphire disk. Free upload, one week left.

**Image:** Disk photo cropped tight to one quadrant where tiles are dense, so the audience can see "I'd live in there."

**Link card subtitle:** Semiconductor lithography means your tile survives in literal gold for a very long time. File locks May 24.

**Destination URL:** `https://southslopenano.com/foundry.html` (recipient: `foundry@`)

**Notes:** "Permanent" + "literal gold" + "one week left" is the urgency stack. Indie-game / sprite-art audiences understand the value of permanence in a way pure-aesthetic audiences may not.

---

## Deployment notes

These are ready to deploy on Reddit Ads once the funding blocker is resolved. Bulk-upload pattern: copy each variant's title/image/subtitle/URL into the cheat-sheet workflow. Conservative rollout: launch Variant A first at $20/day for 24h, then add B and C if A produces email traffic. Cross-check against the existing angle-1/2/3 ads to avoid auction-against-self if running in parallel.
