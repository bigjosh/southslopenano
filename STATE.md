# STATE.md — Live Campaign State

**Last updated:** 2026-05-13 by Claude

---

## Snapshot

- **Sprint timeline:** 11 days to file-lock = 2026-05-24
- **Ad budget:** $1,000 (untouched)
- **Tiles filled:** ~218 of 1,124 at last check — re-verify with live count before any quote
- **Tiles remaining:** ~906
- **Paid orders since campaign start:** 0
- **Free uploads since campaign start:** 0 (campaign hasn't started)
- **South Slope Nano Devices brand:** exists on Stripe; `southslopenano.com` registered by Josh; DNS pointing pending.
- **Product name:** **Mosaic**. Hostname for the upload flow: `mosaic.southslopenano.com`.
- **`claim.html`:** written, committed to repo, NOT yet pointed at by any traffic. Still contains `[FILE-LOCK DATE]` placeholders pending search-replace.
- **Landing page:** not built. Will be served by GH Pages from `docs/` to `southslopenano.com`. Placeholder `docs/index.html` in tree so the GH Pages pipeline can be verified end-to-end before the real page lands.
- **Email gate:** retained. Funnel = `southslopenano.com` → email → emailed upload link → `mosaic.southslopenano.com/upload/claim.html`. No changes to existing upload pipeline.
- **Campaign repo:** this directory is now a git repo (initialized 2026-05-13). No GitHub remote yet.
- **Outbound marketing email:** killed for this campaign. Paid ads replace it.

---

## Open decisions blocking Josh

See `DECISIONS_QUEUE.md` for the full list. Top items:

1. **Real photo of the physical disk** if any exists.

---

## What's done

- Product named **Mosaic** (2026-05-13). Upload-flow subdomain renamed to `mosaic.southslopenano.com` (supersedes the earlier `upload.southslopenano.com` plan from same day). CLAUDE.md updated to reflect.
- Domain `southslopenano.com` registered by Josh (2026-05-13). Matches Stripe LLC descriptor.
- Campaign repo initialized in this directory (`pf-campaign`). `docs/` scaffolded with a placeholder `index.html` so GH Pages can be verified end-to-end before the real landing page lands. `.gitignore` in place. No commits yet — Josh's call when to commit.
- CLAUDE.md updated: `docs/` replaces `landing/` as the landing-source path; Key References section now includes `southslopenano.com` and `upload.southslopenano.com`. Changes in working tree, uncommitted.
- Upload-flow subdomain decided: `upload.southslopenano.com` will CNAME to the existing upload pipeline server. DNS + server-side TLS work owned by Josh. Resolves the cwandt.com-visible-in-email-link concern.
- File-lock date set: 2026-05-24. ~11 days from 2026-05-13. Search-replace `[FILE-LOCK DATE]` in `claim.html` still pending.
- Outbound marketing email channel killed for this campaign. Paid ads (Reddit-led) are the primary acquisition channel; organic is supplemental. Overrides CLAUDE.md's Ring 3 framing where paid was gated on organic signal — flagged to Josh.
- Email gate confirmed to stay. Funnel stays landing → email → emailed upload link → `claim.html`. Existing email-collection pipeline is unchanged; no new form provider, no marketing email layer.
- Landing-page hosting decided: dedicated new domain pointed at a GitHub Pages repo. Allows Claude to update the landing page directly via commits.
- Strategic frame locked: collective-monument angle, white-labeled as South Slope Nano Devices.
- Audience priority locked: pixel-art natives > "one of N" collectors > paid amp.
- `upload-server/claim.html` written and committed to repo on branch `claim-page-rewrite`. Original `upload.html` untouched. Two commits: bare `cp` + the substantive edit, so the diff reviews cleanly.
- $260 CW&T pocket-viewer bundle removed from `claim.html`.
- Honest-notes section added to `claim.html` to inoculate against refund requests.
- Live tile counter wired in `claim.html` via existing `get-parcels` API — no backend changes needed.
- File-lock date placeholder `[FILE-LOCK DATE]` in place in `claim.html`. Search-replace target.

---

## What's in flight

(Nothing — awaiting domain pick to begin action #2, and confirmation of full action set.)

---

## Next 3 actions (proposed 2026-05-13, pending Josh confirmation)

1. **Lock the date in `claim.html`.** Global search-replace `[FILE-LOCK DATE]` → "May 24, 2026" on the `claim-page-rewrite` branch. Mechanical.
2. **Draft the South Slope landing page and set up the GitHub Pages repo to serve it.** Above the fold: live tile counter, scarcity sentence with real date, parcels-grid hero, single email-collection input that hands off to the existing pipeline. Below: fabrication story + FAQ. Source in `landing/`; deployed via GH Pages once Josh registers the domain and points DNS.
3. **Draft 4–6 Reddit Promoted Post creatives across 2–3 angles** for A/B testing days 1–3 — "your tile on a sapphire disk," "1,124 hard cap, file-locks May 24," "fab-engineering-as-art object." Rough budget shape: ~$150–200/day across variants for 3 days, then concentrate the remaining ~$400–600 on the winner. Reddit primary because Ring 1 lives there. Meta/Twitter variants TBD.

---

## Channel checklists (not started)

### Ring 1 — pixel-art / collaborative-canvas

- [ ] r/PixelArt — long-form "we made this weird thing" post
- [ ] r/place follow-up subs — research current activity, post if appropriate
- [ ] Pixilart — community post
- [ ] Lospec forum / Discord — community post
- [ ] Lexaloffle BBS (PICO-8) — community post (they live at 128×128; 500×500 will feel luxurious)
- [ ] Mastodon `#pixelart` — direct posts + outreach to high-follower accounts
- [ ] Bluesky pixel-art crowd — thread

### Ring 2 — "one of N" collectors

- [ ] Show HN draft
- [ ] Pitch email to design newsletters (Sidebar, The Prepared, Kottke — note: Kottke covered the original Pocket Fiche, so there's a news hook)
- [ ] Boing Boing tip
- [ ] Are.na share

### Ring 3 — paid amplification (ELEVATED to primary channel as of 2026-05-13)

- [ ] Reddit Promoted Post creative drafts (4–6 variants across 2–3 angles)
- [ ] Meta and Twitter ad creative variants — TBD
- [ ] $200 reserved for Twitter/X organic-traction amplification if a tweet pops

---

## Decision log (append-only, newest on top)

**2026-05-13** — Product named **Mosaic**. Subdomain for upload flow is `mosaic.southslopenano.com` (supersedes the earlier `upload.southslopenano.com` plan from same day; Josh now wires the hostname based on product name). Picked over Cairn (esoteric / hard to spell), Wafer (semiconductor-honest but less audience-resonant), Quilt, and Slate. Audience resonance with pixel-art primary ring was the tiebreaker.

**2026-05-13** — Campaign repo initialized at `pf-campaign/`. GH Pages will serve `docs/` to `southslopenano.com`. CLAUDE.md convention updated: `docs/` replaces `landing/` as the landing-source path.

**2026-05-13** — Upload subdomain: `upload.southslopenano.com` will CNAME to the existing upload pipeline server. DNS + server-side TLS work owned by Josh. Solves the cwandt.com-visible-in-email-link concern.

**2026-05-13** — Domain selected: `southslopenano.com`. Matches the Stripe LLC descriptor (South Slope Nano Devices, LLC) — URL, brand, and credit card statement all align.

**2026-05-13** — Landing-page hosting: new dedicated domain pointed at a GitHub Pages repo. Lets Claude update the page directly via commits.

**2026-05-13** — Email gate kept. Justified by anti-spam + avoiding work to modify the existing email-collection pipeline. Funnel stays landing → email → emailed upload link → `claim.html`. No new form provider, no marketing email layer.

**2026-05-13** — Outbound marketing email killed for this campaign. Paid ads (Reddit-led) are the primary acquisition channel; organic is supplemental. Strategy: A/B test creative variants in days 1–3, concentrate remaining spend on winners. Overrides CLAUDE.md's original Ring 3 framing where paid was gated on Ring 1+2 organic signal — flagged to Josh for whether to update CLAUDE.md.

**2026-05-13** — File-lock date set to 2026-05-24. ~11 calendar days from decision date.

**2026-05-12** — `claim.html` is the conversion surface, not the landing page. The funnel is landing → email → upload link → upload at `claim.html` → buy from `claim.html`.

**2026-05-12** — Soft-sell funnel chosen: upload is free, payment ask happens immediately after upload on `claim.html`. Predicted to outperform hard-sell on both uploads and paid conversion.

**2026-05-12** — Audiences killed for this sprint: bitcoin/seed-phrase (public viewer breaks privacy), memorial/legacy (wrong timeline), corporate gifts (wrong sales motion), CW&T base (saturated).

**2026-05-12** — `$260` bundle removed from `claim.html`. Disk-only campaign sells $150 disk only.

**2026-05-12** — White-label as South Slope Nano Devices. CW&T not mentioned on campaign surfaces.

**2026-05-12** — `upload.html` is frozen for the duration of the campaign. All campaign work goes in `claim.html`.
