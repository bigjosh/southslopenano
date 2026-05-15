"""
reddit-driver — a thin Playwright wrapper that connects to a Chrome
instance you've already started with --remote-debugging-port and lets
Claude drive the UI one action at a time.

Setup (Josh):
    1. Close all Chrome windows.
    2. Start a dedicated Chrome with remote debugging enabled, using a
       fresh profile directory. From a Windows PowerShell or cmd window:

         "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" ^
           --remote-debugging-port=9222 ^
           --user-data-dir="C:\\chrome-debug-profile"

       (Or any path you don't mind — Chrome will create it fresh.)
    3. In that Chrome window, log in to Reddit + go to ads.reddit.com.
    4. Leave it open. Claude connects to it via CDP and drives.

Usage (Claude):
    python tools/reddit-driver/driver.py goto <url>
    python tools/reddit-driver/driver.py read [filter]
    python tools/reddit-driver/driver.py click <selector>
    python tools/reddit-driver/driver.py fill <selector> <value>
    python tools/reddit-driver/driver.py eval <js>
    python tools/reddit-driver/driver.py tabs

Each invocation: connect via CDP -> run one action -> disconnect ->
print JSON result on stdout. Errors land on stderr with a non-zero
exit code.

Reads:
    "read interactive"  -> only interactive elements (inputs, buttons,
                           links, selects). Cheaper, usually what we want.
    "read all"          -> full DOM-ish accessibility tree.
    "read text"         -> innerText of <body>.
"""

import json
import os
import sys
from playwright.sync_api import sync_playwright


CDP_URL = os.environ.get("CDP_URL", "http://localhost:9222")


def _get_active_page(browser):
    """Pick the most-recently-focused page in the connected browser."""
    pages = []
    for ctx in browser.contexts:
        pages.extend(ctx.pages)
    if not pages:
        raise RuntimeError("No pages found in connected Chrome.")
    # Prefer a page on ads.reddit.com or reddit.com if one exists, else the first.
    for p in pages:
        if "reddit.com" in p.url:
            return p
    return pages[0]


def _print(obj):
    sys.stdout.write(json.dumps(obj, indent=2, ensure_ascii=False))
    sys.stdout.write("\n")


def cmd_tabs(p, _args):
    out = []
    for ctx in p.contexts:
        for page in ctx.pages:
            out.append({"url": page.url, "title": page.title()})
    return {"tabs": out}


def cmd_goto(p, args):
    if not args:
        raise SystemExit("goto requires a URL")
    page = _get_active_page(p)
    page.goto(args[0], wait_until="domcontentloaded", timeout=30000)
    return {"url": page.url, "title": page.title()}


def cmd_read(p, args):
    mode = (args[0] if args else "interactive").lower()
    page = _get_active_page(p)
    if mode == "text":
        return {"url": page.url, "text": page.inner_text("body")[:50000]}
    interactive_only = mode == "interactive"
    js = """(() => {
      const sel = arguments[0]
        ? 'a, button, input, select, textarea, [role=button], [role=link], [contenteditable=true]'
        : 'h1,h2,h3,h4,h5,h6,a,button,input,select,textarea,label,p,li,[role=button],[role=link],[role=heading]';
      const els = [...document.querySelectorAll(sel)];
      return els.slice(0, 400).map((el, i) => {
        const r = el.getBoundingClientRect();
        return {
          i: i,
          tag: el.tagName.toLowerCase(),
          type: el.getAttribute('type') || null,
          name: el.getAttribute('name') || null,
          id: el.id || null,
          role: el.getAttribute('role') || null,
          text: (el.innerText || el.value || el.placeholder || '').slice(0, 200),
          href: el.getAttribute('href') || null,
          visible: r.width > 0 && r.height > 0,
          disabled: el.hasAttribute('disabled')
        };
      });
    })()"""
    page = _get_active_page(p)
    result = page.evaluate(js, interactive_only)
    return {"url": page.url, "title": page.title(), "elements": result}


def cmd_click(p, args):
    if not args:
        raise SystemExit("click requires a selector")
    page = _get_active_page(p)
    page.click(args[0], timeout=15000)
    return {"clicked": args[0], "url": page.url}


def cmd_fill(p, args):
    if len(args) < 2:
        raise SystemExit("fill requires a selector and a value")
    page = _get_active_page(p)
    sel, val = args[0], args[1]
    page.fill(sel, val, timeout=15000)
    return {"filled": sel, "value": val}


def cmd_eval(p, args):
    if not args:
        raise SystemExit("eval requires a JS expression")
    page = _get_active_page(p)
    js = " ".join(args)
    return {"result": page.evaluate(js)}


COMMANDS = {
    "tabs": cmd_tabs,
    "goto": cmd_goto,
    "read": cmd_read,
    "click": cmd_click,
    "fill": cmd_fill,
    "eval": cmd_eval,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in {"-h", "--help", "help"}:
        sys.stdout.write(__doc__)
        sys.exit(0)
    cmd = sys.argv[1].lower()
    if cmd not in COMMANDS:
        sys.stderr.write(f"Unknown command: {cmd}\nKnown: {', '.join(COMMANDS)}\n")
        sys.exit(2)
    args = sys.argv[2:]
    with sync_playwright() as pw:
        try:
            browser = pw.chromium.connect_over_cdp(CDP_URL, timeout=10000)
        except Exception as e:
            sys.stderr.write(
                f"Could not connect to Chrome at {CDP_URL}. "
                f"Is Chrome running with --remote-debugging-port=9222? Error: {e}\n"
            )
            sys.exit(3)
        try:
            result = COMMANDS[cmd](browser, args)
            _print(result)
        except Exception as e:
            sys.stderr.write(f"{type(e).__name__}: {e}\n")
            sys.exit(4)


if __name__ == "__main__":
    main()
