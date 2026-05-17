# mosaic-collect — Cloudflare Worker

Accepts 500×500 1-bit PNG uploads from `southslopenano.com`, stores them in R2, writes metadata to KV. Admin endpoint lists everything as JSON.

## Deploy (one-time, ~20 min in the Cloudflare dashboard)

1. **Cloudflare account.** If you don't have one, sign up at https://dash.cloudflare.com/sign-up (free).

2. **R2: create a bucket.**
   - Dashboard → R2 → Create bucket
   - Name: `mosaic-uploads`
   - Location: Automatic
   - Click Create

3. **KV: create a namespace.**
   - Dashboard → Workers & Pages → KV → Create namespace
   - Name: `mosaic-meta`
   - Click Add

4. **Worker: create it.**
   - Dashboard → Workers & Pages → Create
   - Choose "Create Worker"
   - Name: `mosaic-collect`
   - Click Deploy (with the default Hello World code — we'll replace next)

5. **Paste the Worker code.**
   - On the new Worker's page, click Edit code
   - Replace everything with the contents of `tools/worker/mosaic-collect.js`
   - Click Deploy

6. **Bind R2 to the Worker.**
   - Worker → Settings → Bindings → Add → R2 Bucket
   - Variable name: `R2`
   - R2 bucket: `mosaic-uploads`
   - Save

7. **Bind KV to the Worker.**
   - Worker → Settings → Bindings → Add → KV Namespace
   - Variable name: `KV`
   - KV namespace: `mosaic-meta`
   - Save

8. **Set the admin token.**
   - Generate a long random string somewhere (e.g. `openssl rand -hex 32` or any password manager)
   - Worker → Settings → Variables and Secrets → Add → Type: Secret
   - Variable name: `ADMIN_TOKEN`
   - Value: the random string
   - Save (and stash the value somewhere safe; you'll need it to view uploads)

9. **Note the Worker URL.** It looks like `https://mosaic-collect.<your-subdomain>.workers.dev`. Send that URL back so the landing pages can be wired to call it. (Until that wiring is done, the form submits will fail.)

## Quick smoke test from a terminal

```bash
# Upload a sample PNG (use any small PNG handy)
curl -X POST https://mosaic-collect.<sub>.workers.dev/ \
  -F image=@test.png \
  -F source=sapphire \
  -F email=test@example.com
# expect: {"ok":true,"id":"..."}

# Verify it landed
curl -H "x-admin-token: YOUR_ADMIN_TOKEN" \
  https://mosaic-collect.<sub>.workers.dev/admin
# expect: {"count":1,"items":[{...}]}

# Hit the rate limit
for i in 1 2 3 4; do
  curl -X POST https://mosaic-collect.<sub>.workers.dev/ -F image=@test.png -F source=sapphire
done
# expect 4th call to return 429
```

## Costs

Free tier covers:
- R2: 10 GB storage + 1 M Class A ops/month + 10 M Class B ops/month
- KV: 100k reads + 1k writes per day
- Worker: 100k requests per day

At our expected volume (single-digit thousands of uploads max), we'll sit comfortably inside all free tiers.

## Viewing collected uploads

`GET https://mosaic-collect.<sub>.workers.dev/admin?token=<ADMIN_TOKEN>` returns JSON like:

```json
{
  "count": 12,
  "items": [
    {
      "id": "...",
      "key": "2026-05-17/<id>.png",
      "source": "sapphire",
      "email": "user@example.com",
      "size": 8421,
      "ts": "2026-05-17T14:23:11.000Z",
      "ua": "...",
      "ip_hash": "..."
    },
    ...
  ]
}
```

To download a specific upload: go to Cloudflare dashboard → R2 → `mosaic-uploads` → navigate to `<date>/<id>.png` → Download. (Or I can write a bulk-download script later.)

## What the Worker does NOT do

- No size conversion. The page already converts client-side to 500×500 1-bit PNG before submission.
- No email sending. If you want notifications when uploads arrive, that's a small add-on for v2.
- No integration with the legacy disk pipeline at `mosaic.southslopenano.com`. Deferred until we have a meaningful pile of submissions.
