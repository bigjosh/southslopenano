// mosaic-collect — Cloudflare Worker that accepts 500x500 1-bit PNG
// uploads from the southslopenano.com landing pages, stores them in
// R2, and writes a small metadata record to KV. Also exposes a
// token-protected /admin endpoint that returns all metadata as JSON.
//
// Bindings required:
//   - R2 bucket bound as `R2` (e.g. mosaic-uploads)
//   - KV namespace bound as `KV` (e.g. mosaic-meta)
//   - Secret `ADMIN_TOKEN` (long random string)

const ALLOWED_ORIGINS = new Set([
  "https://southslopenano.com",
  "https://www.southslopenano.com",
]);
const MAX_BYTES = 1024 * 1024;        // 1 MB — converted tiles are tiny
const VALID_MIME = /^image\/png$/i;   // client always submits PNG
const RL_WINDOW = 600;                // 10 min
const RL_MAX = 3;                     // 3 uploads per IP per window
const VALID_SOURCES = new Set([
  "mosaic", "sapphire", "pixel", "tile", "lockin",
  "foundry", "etch", "jb-mosaic", "direct",
]);

function cors(origin) {
  const allow = ALLOWED_ORIGINS.has(origin) ? origin : "https://southslopenano.com";
  return {
    "Access-Control-Allow-Origin": allow,
    "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
    "Access-Control-Allow-Headers": "content-type, x-admin-token",
    "Vary": "Origin",
  };
}

async function sha256(s) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, "0")).join("");
}

function json(body, status, headers) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...headers, "content-type": "application/json" },
  });
}

export default {
  async fetch(req, env) {
    const origin = req.headers.get("Origin") || "";
    const headers = cors(origin);
    const url = new URL(req.url);

    if (req.method === "OPTIONS") {
      return new Response(null, { status: 204, headers });
    }

    // Admin: list collected uploads
    if (url.pathname === "/admin" && req.method === "GET") {
      const tok = req.headers.get("x-admin-token") || url.searchParams.get("token");
      if (tok !== env.ADMIN_TOKEN) {
        return new Response("unauthorized", { status: 401, headers });
      }
      const list = await env.KV.list({ prefix: "u:" });
      const items = await Promise.all(
        list.keys.map(async k => JSON.parse(await env.KV.get(k.name))),
      );
      return json({ count: items.length, items }, 200, headers);
    }

    // Upload
    if (url.pathname === "/" && req.method === "POST") {
      const ip = req.headers.get("CF-Connecting-IP") || "0.0.0.0";
      const rlKey = `rl:${ip}`;
      const cur = parseInt((await env.KV.get(rlKey)) || "0", 10);
      if (cur >= RL_MAX) {
        return json({ error: "rate_limited", retry_after_sec: RL_WINDOW }, 429, headers);
      }

      let form;
      try {
        form = await req.formData();
      } catch {
        return json({ error: "bad_form" }, 400, headers);
      }

      const file = form.get("image");
      const email = (form.get("email") || "").toString().slice(0, 200);
      const srcRaw = (form.get("source") || "direct").toString().toLowerCase();
      const source = VALID_SOURCES.has(srcRaw) ? srcRaw : "direct";

      if (!file || typeof file === "string") {
        return json({ error: "no_image" }, 400, headers);
      }
      if (file.size > MAX_BYTES) {
        return json({ error: "too_large", max_mb: MAX_BYTES / 1024 / 1024 }, 413, headers);
      }
      if (!VALID_MIME.test(file.type)) {
        return json({ error: "bad_type" }, 415, headers);
      }

      const id = crypto.randomUUID();
      const day = new Date().toISOString().slice(0, 10);
      const key = `${day}/${id}.png`;

      await env.R2.put(key, file.stream(), {
        httpMetadata: { contentType: "image/png" },
        customMetadata: { source, email, ip, ts: new Date().toISOString() },
      });

      const ts = new Date().toISOString();
      const meta = {
        id,
        key,
        source,
        email,
        size: file.size,
        ts,
        ua: (req.headers.get("User-Agent") || "").slice(0, 200),
        ip_hash: await sha256(ip + (env.ADMIN_TOKEN || "")),
      };
      await env.KV.put(`u:${ts}:${id}`, JSON.stringify(meta));
      await env.KV.put(rlKey, String(cur + 1), { expirationTtl: RL_WINDOW });

      return json({ ok: true, id }, 200, headers);
    }

    return new Response("not found", { status: 404, headers });
  },
};
