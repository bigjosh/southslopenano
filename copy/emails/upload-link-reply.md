# Upload-link reply template

Sent to users who emailed one of the variant addresses (`request@`, `signup@`, etc.) asking for a Mosaic upload link.

## Workflow

1. User emails one of the variant addresses with an "I plan to upload: …" note (the mailto body is prefilled with that stub).
2. Glance at the note — spam filter, plus a peek at what's coming.
3. Generate an upload code via the existing pipeline.
4. Reply using the body below. Replace `[CODE]`. Add a personal line at the top if their note merited one.

## Subject

> Your Mosaic upload link

## Body

> Thanks — got your request.
>
> Your upload link:
> https://southslopenano.com/upload/claim.html?code=[CODE]
>
> A few quick notes:
>
> - One image per link, 500×500, monochrome. We'll convert anything else as best we can.
> - We review every upload before fabrication. If anything needs adjustment we'll send it back with a note.
> - The disk locks for fabrication on May 24, 2026.
> - The public viewer at https://mosaic.southslopenano.com is permanent — your image lives there regardless of whether you buy a disk.
> - The physical disk is $150 if you want one, but the upload doesn't require buying. The buy button is on the claim page after you upload.
>
> If anything breaks or the link doesn't work, just reply.
>
> Thanks for being part of the run.
>
> — South Slope Nano Devices

## Notes for Josh

- Tone is plainspoken; restraint is the brand voice. No exclamation marks here (one is OK on the landing page CTA per your call, but the reply leans calm).
- The "what's planning" line is intentionally generic so it works whether or not they actually wrote a note.
- The "send it back with a note" sentence sets the moderation precedent gently — establishes that revisions are part of the flow, not a rejection.
- If the request looks like spam (no note, generic burner address), it's fine to ignore — the catch-all setup means we control what counts as legitimate.
