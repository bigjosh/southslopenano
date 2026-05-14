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
- **`claim.html`:** migrated into `docs/upload/claim.html` in this repo. All API calls now absolute to `https://mosaic.southslopenano.com/upload/cgi-bin/app.py`. File-lock date set to May 24, 2026. CW&T-domain leaks removed. Will be served from `https://southslopenano.com/upload/claim.html?code=...` once pushed.
- **Landing page:** Mosaic campaign page lives at `docs/mosaic.html` → `https://southslopenano.com/mosaic.html`. Direct mailto CTA to `mosaic@southslopenano.com` (subject "Mosaic upload link request", body prefilled with "I plan to upload: "). User clicks, email client opens, they describe their image and send. Spam control + idea-fishing. Functional end-to-end pending the mailbox.
- **Home page:** `docs/index.html` → `https://southslopenano.com/` is a generic South Slope Nano Devices landing — one paragraph describing the company (nano-lithography arm of Gotham Silicon, Columbia Nano Initiative clean room, NYC), plus a Projects section with two cards: **Mosaic** (links to `/mosaic.html`) and **Pi Plate** (links to Josh's writeup at `wp.josh.com/2025/10/30/...`).
- **Email gate:** retained. Funnel = `southslopenano.com` → email → emailed upload link → `southslopenano.com/upload/claim.html?code=...` (our migrated copy; cross-origin API calls to `mosaic.southslopenano.com` are CORS-greenlit).
- **Campaign repo:** `https://github.com/bigjosh/southslopenano` (public). Initial commit pushed 2026-05-13. GH Pages config pending Josh (Settings → Pages → main / `docs`).
- **Outbound marketing email:** killed for this campaign. Paid ads replace it.

---

## Open decisions blocking Josh

See `DECISIONS_QUEUE.md` for the full list. Top items:

1. **Real photo of the physical disk** if any exists.

---

## What's done

- Landing page drafted at `docs/index.html` — replaces the placeholder. Live tile counter, scarcity sentence with real date, hero (disk render), email-collection form, fabrication story, honest-notes. Open Graph / Twitter card meta tags included.
- Upload-link reply template drafted at `copy/emails/upload-link-reply.md`. Standard body Josh uses when replying to inbound `request@/signup@/etc.` emails with a generated upload code. Plainspoken; sets moderation precedent gently; mentions the $150 disk option without leading with it.
- Mosaic landing copy + CSS pass (mobile-friendly): bumped body to 1.125rem (~18px), removed orphan form/input styles, used clamp() for responsive h1, added 520px breakpoint to tighten padding. Copy fixes: "physical disk afterward" → "physical object afterwards"; clarified that only buyers get the physical object (was implying all contributors get one); added "Be cool and creative." to the moderation note; dropped the exclamation on the CTA paragraph per the default brand voice. All 6 variant pages regenerated from the new `mosaic.html`.
- Variant attribution implemented as 6 thin per-variant landing pages, each a duplicate of `mosaic.html` with one line changed (the mailto recipient). Pages: `/tile.html` (`tile@`), `/pixel.html` (`pixel@`), `/sapphire.html` (`sapphire@`), `/lockin.html` (`lockin@`), `/foundry.html` (`foundry@`), `/etch.html` (`etch@`). `mosaic.html` stays as canonical with `mosaic@` for direct/typed-in traffic. Each Reddit ad variant points at its own slug; To: header on inbound email tells Josh which variant generated it. **Maintenance:** when `mosaic.html` changes, propagate to the 6 variants (re-run the cp+sed pattern in the variant-generation commit). Manual sync acceptable for a 1-week campaign; if it gets painful, automate via a build step.
- Mosaic landing renamed from `docs/index.html` to `docs/mosaic.html`. Direct mailto CTA (no JS form handler). Subject "Mosaic upload link request", body prefilled with "I plan to upload: ". Ad creatives' destination URL updated to `https://southslopenano.com/mosaic.html`.
- New home page at `docs/index.html`: minimal page describing South Slope Nano Devices as the nano-lithography arm of Gotham Silicon, operating inside the Columbia Nano Initiative clean room in NYC. Includes a card linking to the Mosaic campaign. Lets the apex domain serve as a brand homepage even after this campaign concludes.
- Email-collection mechanism: mailto. CTA opens user's default email client with To=`mosaic@southslopenano.com`, Subject="Mosaic upload link request", Body prefilled with "I plan to upload: ". Josh receives, replies with upload link via existing pipeline. Cheap v1; iterate if conversion is poor or volume hits manual-bottleneck.
- Reddit Promoted Post creatives drafted at `copy/ads/reddit/`. 3 angles × 2 variants = 6 ads, plus a README with the test plan and subreddit lists. Angles: (1) "your tile on a sapphire disk" for pixel-art audiences, (2) "1,124 hard cap, file-locks May 24" for scarcity-driven collectors, (3) "semiconductor fab as art press" for engineers/makers. Ready to feed into Reddit ad UI once Josh greenlights the run and an ad account is set up.
- `claim.html` migrated from the cwandt repo into `docs/upload/claim.html`. 12 spots rewritten: 3 fetch API URLs absolutized to `https://mosaic.southslopenano.com/upload/cgi-bin/app.py`; 2 `window.location.origin` hardcoded; 3 asset/link URLs absolutized (`style.css`, `disk.png`, viewer link); 1 `[FILE-LOCK DATE]` placeholder replaced with `May 24, 2026`; CW&T-branded guide link dropped; `pf.cwandt.com` mention in honest-notes redirected to `mosaic.southslopenano.com`. Verified no cwandt/pocketfiche references remain and no relative URLs left.
- GH Pages live: `bigjosh/southslopenano` serves `docs/` to `southslopenano.com` (Josh configured 2026-05-13). Placeholder `docs/index.html` is what's currently served; will be replaced by the real landing page.
- Campaign repo published as `bigjosh/southslopenano` (public, 2026-05-13). Initial commit contains CLAUDE.md, STATE.md, DECISIONS_QUEUE.md, `docs/index.html` placeholder, `.gitignore`.
- CORS header (`Access-Control-Allow-Origin: *`) live on the `mosaic.southslopenano.com` upload server. Verified by direct GET + OPTIONS preflight — both return correct CORS headers. Cross-origin calls from a future `claim.html` hosted on `southslopenano.com` will work.
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

**2026-05-13** — Variant attribution finalized: six thin landing pages (`/tile.html`, `/pixel.html`, `/sapphire.html`, `/lockin.html`, `/foundry.html`, `/etch.html`), each a copy of `/mosaic.html` with a different mailto recipient. Each Reddit variant points at its own slug; the To: header of inbound mail attributes it. Picked over UTM codes (words read better) and a single-page-with-JS approach (multiple pages are subtler — URLs look like normal site sections, not tracking links). Trade-off: copy changes need to propagate to 6 files; manual sync is acceptable for a 1-week campaign.

**2026-05-13** — Mosaic landing moved to `/mosaic.html`; apex `/` is now a generic South Slope Nano Devices home page. Reason: campaign-specific copy was sitting on the front door; the apex is reusable for future projects once Mosaic concludes. Ad creatives' destination URL updated to `https://southslopenano.com/mosaic.html`.

**2026-05-13** — CTA on Mosaic landing simplified from form-with-input to a direct mailto link. Reasoning: the user's email address is already in the From: header when they send; the form input added friction without adding signal. The mailto body is prefilled with "I plan to upload: " as a cursor-position hint.

**2026-05-13** — Email-collection mechanism chosen: mailto to `mosaic@southslopenano.com` with subject "Mosaic upload link request". Picked over third-party form services and a custom backend endpoint: zero new infrastructure, easy to iterate. Conversion tracking is "count inbox / count spend"; Reddit pixel-based tracking would require a thank-you page (deferred).

**2026-05-13** — Landing page and Reddit ad creatives drafted. Landing page at `docs/index.html` (replaces placeholder); ad creatives at `copy/ads/reddit/` (6 variants across 3 angles). Both pending Josh's review. Landing page is blocked from real traffic until the email-collection endpoint is chosen and wired (new DECISIONS_QUEUE entry).

**2026-05-13** — Viewer CW&T-branding decision: live with it (option C). The viewer at `mosaic.southslopenano.com/` still shows "Welcome to the CW&T pocket fiche project" banner. Josh's call. Most buyers won't read the banner closely; cost of editing the cwandt repo's viewer wasn't worth it for this campaign.

**2026-05-13** — `claim.html` migration executed. Lives at `docs/upload/claim.html` in this repo, served via GH Pages at `southslopenano.com/upload/claim.html`. API calls go cross-origin to `mosaic.southslopenano.com`; CORS allows it. Removed the CW&T-branded guide link entirely; pointed honest-notes viewer mention at `mosaic.southslopenano.com` instead of `pf.cwandt.com`. Note: the viewer at `mosaic.southslopenano.com` still has CW&T banner branding — separate decision pending Josh (edit cwandt viewer repo / drop the link / live with it).

**2026-05-13** — Campaign repo published as `bigjosh/southslopenano` (public). Initial commit pushed. Picked over `bigjosh/mosaic` and `bigjosh/pf-campaign`; domain-matched name is most legible publicly.

**2026-05-13** — `claim.html` will move into this repo's `docs/upload/claim.html` rather than staying in the cwandt repo. Enabled by Josh adding `Access-Control-Allow-Origin: *` on the `mosaic.southslopenano.com` upload server. Five rewrites needed in `claim.html` when migrating: 3 relative fetch URLs → absolute (`https://mosaic.southslopenano.com/upload/cgi-bin/app.py...`), 2 `window.location.origin` refs → hardcoded `https://mosaic.southslopenano.com`. Stale-fact: STATE.md previously named branch `claim-page-rewrite` in cwandt repo — that branch doesn't exist; `claim.html` is on `main`. Migration path replaces the PR-to-cwandt-repo workflow entirely.

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
