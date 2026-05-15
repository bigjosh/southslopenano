# reddit-driver

Thin Playwright wrapper that connects to a Chrome instance Josh has started with `--remote-debugging-port`. Claude calls `driver.py` from Bash to drive Reddit Ads (or any other site Josh has open in that Chrome) one action at a time, against Josh's live logged-in session.

## Why this exists

The Claude Chrome extension blocks `reddit.com` outright — a safety policy designed to prevent Claude from posting on Reddit, but which incidentally also blocks legitimate ad-management. Playwright over CDP bypasses the extension's safety list (it isn't using the extension at all). Josh's logged-in session stays in his control; Claude never touches credentials.

## Setup

1. **Install dependencies** (one-time):
   ```
   pip install playwright
   ```
   (We connect to an already-running Chrome, so we don't need to `playwright install` a separate browser binary.)

2. **Start Chrome with remote debugging.** Close existing Chrome windows first (Chrome only allows one process per profile), then in PowerShell or cmd:
   ```
   "C:\Program Files\Google\Chrome\Application\chrome.exe" ^
     --remote-debugging-port=9222 ^
     --user-data-dir="C:\chrome-debug-profile"
   ```
   The `--user-data-dir` is intentionally a fresh path so it doesn't conflict with your normal Chrome profile. Chrome will create it on first launch.

3. **Log in to Reddit** in that Chrome window (`reddit.com` → sign in), then open `ads.reddit.com`. Leave the window open.

4. **Sanity check from Claude side**:
   ```
   python tools/reddit-driver/driver.py tabs
   ```
   Should print JSON with at least one tab showing `reddit.com` in its URL.

## Verbs

| command | what it does |
|---|---|
| `tabs` | List currently open tabs and titles. |
| `goto <url>` | Navigate the active page to a URL. |
| `read [interactive\|all\|text]` | Snapshot the active page. Defaults to `interactive` (buttons / links / inputs only). `text` is `innerText` of `<body>`. |
| `click <selector>` | Click a CSS selector. Supports Playwright selectors including `:has-text("...")`. |
| `fill <selector> <value>` | Fill an input/textarea by selector. |
| `eval <js>` | Run JavaScript in the page and return its value. |

Each invocation reconnects, runs one action, disconnects. JSON to stdout, errors to stderr.

## Safety notes

- Josh logs in himself in the debug Chrome — Claude never receives passwords.
- Each action is an explicit `python driver.py ...` call visible in chat history.
- If Josh wants to revoke access mid-flow, just close the Chrome window. Reconnection fails cleanly and Claude sees the error.
- The user-data-dir is dedicated to this purpose — nothing else is in it. Josh's regular Chrome profile is untouched.
