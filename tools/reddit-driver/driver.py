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
from pathlib import Path
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
    js = """(interactiveOnly) => {
      const sel = interactiveOnly
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
    }"""
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


def cmd_type(p, args):
    """type <selector> <text> — focuses the selector, then simulates real
    keystrokes (vs fill() which just sets value). Required for react-select
    and other components that watch for input events to show autocomplete."""
    if len(args) < 2:
        raise SystemExit("type requires a selector and a value")
    page = _get_active_page(p)
    sel, val = args[0], args[1]
    page.locator(sel).first.click(timeout=10000)
    page.keyboard.type(val, delay=20)
    return {"typed": sel, "value": val}


def cmd_press(p, args):
    """press <key> — send a single key like Enter, Escape, Tab, ArrowDown.
    Optional second arg is a selector to focus first."""
    if not args:
        raise SystemExit("press requires a key")
    page = _get_active_page(p)
    if len(args) >= 2:
        page.locator(args[1]).first.focus(timeout=10000)
    page.keyboard.press(args[0])
    return {"pressed": args[0]}


def cmd_screenshot(p, args):
    """screenshot [path] — save a PNG of the active page. Defaults to
    tools/reddit-driver/.screenshots/latest.png so Claude can Read it."""
    page = _get_active_page(p)
    here = Path(__file__).resolve().parent
    out_dir = here / ".screenshots"
    out_dir.mkdir(exist_ok=True)
    path = Path(args[0]) if args else out_dir / "latest.png"
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    page.screenshot(path=str(path), full_page=False)
    return {"saved": str(path), "viewport": page.viewport_size or "(unknown)"}


def cmd_click_at(p, args):
    """click_at <x> <y> — real-mouse click at viewport coordinates.
    Triggers proper native events; works with react-select etc. that
    ignore synthetic events."""
    if len(args) < 2:
        raise SystemExit("click_at requires x and y")
    x = float(args[0])
    y = float(args[1])
    page = _get_active_page(p)
    page.mouse.click(x, y)
    return {"clicked_at": [x, y]}


def cmd_move_to(p, args):
    """move_to <x> <y> — move mouse without clicking (hover)."""
    if len(args) < 2:
        raise SystemExit("move_to requires x and y")
    x = float(args[0])
    y = float(args[1])
    page = _get_active_page(p)
    page.mouse.move(x, y)
    return {"moved_to": [x, y]}


def cmd_upload(p, args):
    """upload <selector> <path> — set a file on a (possibly hidden)
    <input type=file>. Selector can be the input itself or use the nth
    pattern e.g. 'input[type=file] >> nth=0'."""
    if len(args) < 2:
        raise SystemExit("upload requires a selector and a file path")
    sel, path = args[0], args[1]
    page = _get_active_page(p)
    page.locator(sel).first.set_input_files(path)
    return {"uploaded": path, "to": sel}


COMMANDS = {
    "tabs": cmd_tabs,
    "goto": cmd_goto,
    "read": cmd_read,
    "click": cmd_click,
    "fill": cmd_fill,
    "eval": cmd_eval,
    "type": cmd_type,
    "press": cmd_press,
    "screenshot": cmd_screenshot,
    "click_at": cmd_click_at,
    "move_to": cmd_move_to,
    "upload": cmd_upload,
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
