// mosaic-collect — Cloudflare Worker that accepts 500x500 1-bit PNG
// uploads from the southslopenano.com landing pages, stores them in
// R2, and writes a small metadata record to KV.
//
// Endpoints:
//   POST /                          — receive an upload
//   GET  /admin?token=X             — HTML gallery (default)
//   GET  /admin?token=X&format=json — JSON metadata
//   GET  /img/<r2-key>?token=X      — proxy image bytes from R2
//   POST /delete?token=X&kv=<key>&r2=<key>
//                                   — remove an upload (both R2 + KV)
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

function checkAdmin(req, url, env) {
  const tok = req.headers.get("x-admin-token") || url.searchParams.get("token");
  return tok === env.ADMIN_TOKEN;
}

function esc(s) {
  return String(s).replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

function renderGallery(items, token) {
  const tEnc = encodeURIComponent(token);
  const sources = [...new Set(items.map(i => i.source))].sort();
  const total = items.length;

  const itemHtml = items.length === 0
    ? `<p class="empty">No uploads yet. When someone submits an image through a landing-page form, it'll appear here.</p>`
    : items.map(it => `
        <figure class="tile" data-source="${esc(it.source)}">
          <a href="/img/${encodeURIComponent(it.key)}?token=${tEnc}" target="_blank">
            <img src="/img/${esc(it.key)}?token=${tEnc}" alt="upload from ${esc(it.source)}" loading="lazy">
          </a>
          <figcaption>
            <span class="src src-${esc(it.source)}">${esc(it.source)}</span>
            <time>${esc(it.ts.slice(0, 19).replace("T", " "))} UTC</time>
            ${it.email ? `<a class="email" href="mailto:${esc(it.email)}">${esc(it.email)}</a>` : `<span class="email muted">(no email)</span>`}
            <span class="size muted">${Math.round(it.size / 1024 * 10) / 10} KB</span>
          </figcaption>
          <button class="del" data-kv="${esc(it.kvKey)}" data-r2="${esc(it.key)}">Delete</button>
        </figure>
      `).join("");

  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="robots" content="noindex,nofollow">
  <title>Mosaic uploads — ${total}</title>
  <style>
    *,*::before,*::after { box-sizing: border-box; }
    html,body { margin: 0; padding: 0; }
    body {
      background: #0a0a0a; color: #f1f1f1;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
      line-height: 1.5;
    }
    header {
      padding: 20px 24px;
      border-bottom: 1px solid #2a2a2a;
      display: flex; flex-wrap: wrap; gap: 16px; align-items: baseline;
    }
    h1 { font-size: 1.4rem; margin: 0; }
    .count { color: #00ffff; font-weight: 600; }
    .filters {
      display: flex; gap: 6px; flex-wrap: wrap; margin-left: auto;
    }
    .filters button {
      background: #141414; border: 1px solid #2a2a2a; color: #ccc;
      padding: 4px 10px; border-radius: 4px; cursor: pointer;
      font-family: inherit; font-size: 0.85rem;
    }
    .filters button.active { background: #00ffff; color: #000; border-color: #00ffff; }
    .filters button:hover:not(.active) { border-color: #00ffff; color: #fff; }
    main {
      padding: 20px 24px;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
      gap: 18px;
    }
    .tile {
      background: #141414; border: 1px solid #2a2a2a; border-radius: 6px;
      margin: 0; padding: 12px; position: relative;
    }
    .tile img {
      width: 100%; aspect-ratio: 1/1; display: block;
      background: #fff; image-rendering: pixelated; border-radius: 4px;
    }
    figcaption {
      margin-top: 10px;
      display: flex; flex-wrap: wrap; gap: 6px 10px;
      font-size: 0.82rem;
    }
    .src {
      background: rgba(0,255,255,0.15); color: #00ffff;
      padding: 2px 8px; border-radius: 3px; font-weight: 600;
    }
    time { color: #aaa; }
    .email { color: #00ffff; text-decoration: none; word-break: break-all; }
    .email:hover { text-decoration: underline; }
    .muted { color: #888; }
    .size { margin-left: auto; }
    .del {
      position: absolute; top: 8px; right: 8px;
      background: rgba(20,20,20,0.85); color: #ff6b6b;
      border: 1px solid #3a1a1a; border-radius: 4px;
      padding: 4px 10px; font-size: 0.75rem; cursor: pointer;
      opacity: 0; transition: opacity .15s;
      font-family: inherit;
    }
    .tile:hover .del { opacity: 1; }
    .del:hover { background: #2a0a0a; color: #fff; }
    .empty { color: #888; text-align: center; padding: 60px 20px; grid-column: 1/-1; }
    .json-link { color: #aaa; font-size: 0.85rem; }
    .json-link:hover { color: #00ffff; }
  </style>
</head>
<body>
  <header>
    <h1>Mosaic uploads <span class="count">${total}</span></h1>
    <div class="filters" id="filters">
      <button class="active" data-src="">All</button>
      ${sources.map(s => `<button data-src="${esc(s)}">${esc(s)}</button>`).join("")}
    </div>
    <a class="json-link" href="?token=${tEnc}&format=json">view JSON</a>
  </header>
  <main id="grid">${itemHtml}</main>
  <script>
    const tok = ${JSON.stringify(token)};
    const tiles = [...document.querySelectorAll(".tile")];
    document.getElementById("filters").addEventListener("click", e => {
      if (e.target.tagName !== "BUTTON") return;
      document.querySelectorAll("#filters button").forEach(b => b.classList.toggle("active", b === e.target));
      const want = e.target.dataset.src;
      tiles.forEach(t => { t.style.display = (!want || t.dataset.source === want) ? "" : "none"; });
    });
    document.addEventListener("click", async e => {
      if (!e.target.classList.contains("del")) return;
      if (!confirm("Delete this upload? This cannot be undone.")) return;
      const kv = e.target.dataset.kv;
      const r2 = e.target.dataset.r2;
      const r = await fetch("/delete?token=" + encodeURIComponent(tok)
        + "&kv=" + encodeURIComponent(kv)
        + "&r2=" + encodeURIComponent(r2), { method: "POST" });
      if (r.ok) e.target.closest(".tile").remove();
      else alert("Delete failed: " + r.status);
    });
  </script>
</body>
</html>`;
}

export default {
  async fetch(req, env) {
    const origin = req.headers.get("Origin") || "";
    const headers = cors(origin);
    const url = new URL(req.url);

    if (req.method === "OPTIONS") {
      return new Response(null, { status: 204, headers });
    }

    // Admin: HTML gallery (default) or JSON
    if (url.pathname === "/admin" && req.method === "GET") {
      if (!checkAdmin(req, url, env)) {
        return new Response("unauthorized", { status: 401, headers });
      }
      const list = await env.KV.list({ prefix: "u:" });
      const items = await Promise.all(
        list.keys.map(async k => {
          const v = JSON.parse(await env.KV.get(k.name));
          v.kvKey = k.name;
          return v;
        }),
      );
      // Newest first.
      items.sort((a, b) => (b.ts || "").localeCompare(a.ts || ""));

      if (url.searchParams.get("format") === "json") {
        return json({ count: items.length, items }, 200, headers);
      }

      const token = req.headers.get("x-admin-token") || url.searchParams.get("token");
      return new Response(renderGallery(items, token), {
        status: 200,
        headers: { ...headers, "content-type": "text/html; charset=utf-8" },
      });
    }

    // Image proxy: stream an R2 object's bytes through, gated by admin token.
    if (url.pathname.startsWith("/img/") && req.method === "GET") {
      if (!checkAdmin(req, url, env)) {
        return new Response("unauthorized", { status: 401, headers });
      }
      const key = decodeURIComponent(url.pathname.slice("/img/".length));
      const obj = await env.R2.get(key);
      if (!obj) return new Response("not found", { status: 404, headers });
      return new Response(obj.body, {
        status: 200,
        headers: {
          ...headers,
          "content-type": obj.httpMetadata?.contentType || "image/png",
          "cache-control": "private, max-age=300",
        },
      });
    }

    // Delete: remove R2 object + KV record together.
    if (url.pathname === "/delete" && req.method === "POST") {
      if (!checkAdmin(req, url, env)) {
        return new Response("unauthorized", { status: 401, headers });
      }
      const kvKey = url.searchParams.get("kv");
      const r2Key = url.searchParams.get("r2");
      if (!kvKey || !r2Key) {
        return json({ error: "missing_keys" }, 400, headers);
      }
      // Safety: only allow deleting upload entries (prefix u:) and not rate-limit keys etc.
      if (!kvKey.startsWith("u:")) {
        return json({ error: "bad_kv_key" }, 400, headers);
      }
      await Promise.all([
        env.R2.delete(r2Key),
        env.KV.delete(kvKey),
      ]);
      return json({ ok: true }, 200, headers);
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
