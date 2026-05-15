# Reddit Ads — initial launch cheat sheet

Copy-paste targets for the Reddit Ads UI. Account: **Gotham Silicon Ad Account**.

Start with **two ads** under one campaign — different audience, different angle. Read which works in 48 hours, then scale.

## Campaign settings

| field | value |
|---|---|
| Campaign name | `Mosaic launch — 2026-05 first wave` |
| Objective | **Traffic** (Reddit calls it "Send people to a website") |
| Funding source | the one already attached to Gotham Silicon |
| Total campaign budget | leave blank (lifetime) OR set $300 if it forces one |

---

## Ad Group 1 — Scarcity hook

| field | value |
|---|---|
| Ad group name | `Scarcity — r/InternetIsBeautiful + r/Art` |
| Daily budget | **$25** |
| Schedule | start: now · end: **2026-05-23** (one day before file-lock) |
| Bidding | **Cost cap** at $1.50 CPC (raise if it doesn't spend) |
| Goal | Clicks |
| Subreddit targeting | `r/InternetIsBeautiful`, `r/Art`, `r/somethingimade`, `r/woahdude`, `r/Aesthetic` |
| Interest targeting | leave off — subreddit targeting only |
| Location | United States, Canada, UK, Australia |
| Devices | All |

### Ad 1 (Scarcity)

| field | value |
|---|---|
| Ad name | `A2V1 — 1,124 cap` |
| Format | **Image post** |
| Headline | `1,124 tiles on a 29mm sapphire disk. ~906 left. File locks May 24.` |
| Destination URL | `https://southslopenano.com/sapphire.html` |
| Image | `disk-photo.jpg` from `docs/` in the repo (already on disk; Reddit will require a fresh upload) |
| Call to action button | **Learn More** |
| Display name | `South Slope Nano Devices` |

---

## Ad Group 2 — r/place hook

| field | value |
|---|---|
| Ad group name | `r/place — r/PixelArt + r/place` |
| Daily budget | **$25** |
| Schedule | start: now · end: **2026-05-23** |
| Bidding | **Cost cap** at $1.50 CPC |
| Goal | Clicks |
| Subreddit targeting | `r/PixelArt`, `r/place`, `r/Aseprite`, `r/PICO8`, `r/IndieDev` |
| Interest targeting | leave off |
| Location | United States, Canada, UK, Australia |
| Devices | All |

### Ad 2 (r/place analogy)

| field | value |
|---|---|
| Ad name | `A1V2 — like r/place` |
| Format | **Image post** |
| Headline | `Place a 500×500 image on a permanent shared disk. Like r/place, but it ships to your door.` |
| Destination URL | `https://southslopenano.com/pixel.html` |
| Image | `disk-photo.jpg` (same image for both — title is the variable being tested) |
| Call to action button | **Learn More** |
| Display name | `South Slope Nano Devices` |

---

## After Reddit's ad review (typically 2–24 hours)

Both go live. Monitor in Reddit Ads dashboard:

- **CTR** — clicks divided by impressions. Reddit ads typically run 0.2–0.8% CTR. Anything ≥0.5% is signal.
- **Cost per click** — should land $0.40–$1.50 in these subs. If you're hitting the cap with no spend, raise the cap to $2.00.
- **Email inbox volume** — count emails per variant address (`sapphire@`, `pixel@`) per day. That's the actual conversion event.

## Iteration playbook (next 48h)

When one ad clearly outperforms (let's say `sapphire@` is getting 3× the email volume of `pixel@`), tell me:

> "Sapphire is winning, kill pixel and scale sapphire to $50/day"

I'll send back a one-paragraph instruction list ("In Reddit Ads UI: open ad group X → daily budget → change to 50 → pause ad group Y"). One minute of your time per iteration.

If you want to swap a title without me drafting fresh, replace the current one with another variant from `angle-1-your-tile.md`, `angle-2-scarcity.md`, or `angle-3-fab-as-art.md`.

## What I'd want to know after launch

Reply here with anything useful:
- Reddit's reported "estimated daily reach" when you save the ad group (informs whether targeting is too narrow)
- Whether either ad was rejected by Reddit's reviewer (and the reason)
- First 6-12 hours of CTR + impression data
- Email volume per variant address by end of day 1
