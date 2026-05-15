"""
Mosaic inbox — local web UI for handling upload-link requests.

Reads unread mail from the mosaic@southslopenano.com IMAP inbox, lets
Josh review each message, generates an upload code via the upload-server
API, sends the reply via SMTP, then moves the inbound message to a
"Replied" folder.

Run:
    pip install -r requirements.txt
    cp config.example.json config.json   # then fill in real creds
    python app.py
Open http://127.0.0.1:5000

The reply body is read at runtime from
    copy/emails/upload-link-reply.md
so edits to the template propagate without restarting the server.
"""

import email
import imaplib
import json
import re
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formatdate, make_msgid, parseaddr
from html.parser import HTMLParser
from pathlib import Path

import requests
from flask import Flask, render_template, request, redirect, url_for, flash


# ----------------------------------------------------------------------------
# HTML -> plain text
# ----------------------------------------------------------------------------

_BLOCK_TAGS = {"br", "p", "li", "div", "tr", "h1", "h2", "h3", "h4", "h5", "h6"}
_SKIP_TAGS = {"script", "style", "head", "title"}


class _HTMLToText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in _SKIP_TAGS:
            self._skip_depth += 1
        elif tag in _BLOCK_TAGS and self._skip_depth == 0:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in _SKIP_TAGS:
            self._skip_depth = max(0, self._skip_depth - 1)
        elif tag in _BLOCK_TAGS and self._skip_depth == 0:
            self.parts.append("\n")

    def handle_data(self, data):
        if self._skip_depth == 0:
            self.parts.append(data)

    def get_text(self):
        text = "".join(self.parts)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n\s*\n+", "\n\n", text)
        return text.strip()


def html_to_text(s):
    p = _HTMLToText()
    p.feed(s)
    p.close()
    return p.get_text()


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
TEMPLATE_PATH = REPO_ROOT / "copy" / "emails" / "upload-link-reply.md"
CONFIG_PATH = HERE / "config.json"

app = Flask(__name__)
app.secret_key = "mosaic-inbox-local-only"


@app.context_processor
def inject_globals():
    return {"config_imap_user": CONFIG.get("imap_user", "")}


def load_config():
    if not CONFIG_PATH.exists():
        raise SystemExit(
            f"config.json not found at {CONFIG_PATH}. "
            f"Copy config.example.json -> config.json and fill in real values."
        )
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


CONFIG = load_config()


# ----------------------------------------------------------------------------
# Reply template parsing
# ----------------------------------------------------------------------------

def read_reply_template():
    """Pull `## Subject` and `## Body` out of the markdown template.

    Each section is a blockquote (lines starting with `> `). Blank lines
    OUTSIDE blockquotes are tolerated (markdown allows whitespace between
    a heading and its blockquote) and don't end the section. Only a new
    `## ` heading or a non-quote non-blank line ends it.
    """
    text = TEMPLATE_PATH.read_text(encoding="utf-8")
    subject_lines, body_lines = [], []
    section = None
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("## "):
            heading = stripped[3:].strip().lower()
            if heading == "subject":
                section = "subject"
            elif heading == "body":
                section = "body"
            else:
                section = None
            continue
        if section is None:
            continue
        if stripped.startswith("> "):
            line = stripped[2:]
        elif stripped == ">":
            line = ""
        elif stripped == "":
            # Blank lines don't end the section — markdown often puts one
            # between a heading and its blockquote.
            continue
        else:
            section = None
            continue
        if section == "subject":
            subject_lines.append(line)
        else:
            body_lines.append(line)
    subject = " ".join(s.strip() for s in subject_lines if s.strip())
    body = "\n".join(body_lines).strip("\n") + "\n"
    return subject, body


# ----------------------------------------------------------------------------
# IMAP helpers
# ----------------------------------------------------------------------------

def imap_connect():
    M = imaplib.IMAP4_SSL(CONFIG["imap_host"], CONFIG.get("imap_port", 993))
    M.login(CONFIG["imap_user"], CONFIG["imap_pass"])
    return M


def _decode_payload(part):
    charset = part.get_content_charset() or "utf-8"
    payload = part.get_payload(decode=True) or b""
    return payload.decode(charset, errors="replace")


def _extract_body(msg):
    """Return plain text for display. Prefer text/plain. If only HTML is
    available, strip tags + decode entities so it's readable."""
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            disp = str(part.get("Content-Disposition", ""))
            if ct == "text/plain" and "attachment" not in disp:
                return _decode_payload(part)
        for part in msg.walk():
            if part.get_content_type() == "text/html":
                return html_to_text(_decode_payload(part))
        return ""
    ct = msg.get_content_type()
    raw = _decode_payload(msg)
    if ct == "text/html":
        return html_to_text(raw)
    return raw


def fetch_pending():
    """Return all messages in INBOX as dicts (pending = anything not yet moved to Replied)."""
    out = []
    M = imap_connect()
    try:
        M.select("INBOX")
        typ, data = M.uid("SEARCH", None, "ALL")
        if typ != "OK" or not data or not data[0]:
            return out
        uids = data[0].split()
        for uid in uids:
            typ, msg_data = M.uid("FETCH", uid, "(BODY.PEEK[])")
            if typ != "OK" or not msg_data or not isinstance(msg_data[0], tuple):
                continue
            raw = msg_data[0][1]
            msg = email.message_from_bytes(raw)
            out.append({
                "uid": uid.decode(),
                "from_addr": parseaddr(msg.get("From", ""))[1],
                "from_name": parseaddr(msg.get("From", ""))[0],
                "to_addr": parseaddr(msg.get("To", ""))[1],
                "subject": msg.get("Subject", ""),
                "date": msg.get("Date", ""),
                "body": _extract_body(msg).strip(),
                "message_id": msg.get("Message-ID", ""),
                "references": msg.get("References", ""),
            })
    finally:
        M.logout()
    return out


def fetch_one(uid):
    M = imap_connect()
    try:
        M.select("INBOX")
        typ, msg_data = M.uid("FETCH", uid, "(BODY.PEEK[])")
        if typ != "OK" or not msg_data or not isinstance(msg_data[0], tuple):
            return None
        raw = msg_data[0][1]
        msg = email.message_from_bytes(raw)
        return {
            "uid": uid,
            "from_addr": parseaddr(msg.get("From", ""))[1],
            "from_name": parseaddr(msg.get("From", ""))[0],
            "to_addr": parseaddr(msg.get("To", ""))[1],
            "subject": msg.get("Subject", ""),
            "date": msg.get("Date", ""),
            "body": _extract_body(msg).strip(),
            "message_id": msg.get("Message-ID", ""),
            "references": msg.get("References", ""),
        }
    finally:
        M.logout()


def move_to_folder(uid, folder):
    """Move UID from INBOX to <folder>, creating the folder if needed. Marks Seen along the way."""
    M = imap_connect()
    try:
        M.select("INBOX")
        M.create(folder)  # silently no-op if it already exists
        M.uid("STORE", uid, "+FLAGS", "(\\Seen)")
        copy_typ, _ = M.uid("COPY", uid, folder)
        if copy_typ == "OK":
            M.uid("STORE", uid, "+FLAGS", "(\\Deleted)")
            M.expunge()
    finally:
        M.logout()


def mark_handled(uid):
    move_to_folder(uid, "Replied")


# ----------------------------------------------------------------------------
# Upload-server API
# ----------------------------------------------------------------------------

def generate_upload_code(backer_email):
    r = requests.post(
        CONFIG["generate_code_url"],
        data={
            "command": "generate-code",
            "admin-id": CONFIG["admin_id"],
            "backer-id": backer_email,
            "notes": "Mosaic",
        },
        timeout=20,
    )
    r.raise_for_status()
    payload = r.json()
    if payload.get("status") != "success":
        raise RuntimeError(f"generate-code failed: {payload}")
    return payload["code"]


# ----------------------------------------------------------------------------
# SMTP
# ----------------------------------------------------------------------------

def send_reply(to_addr, subject, body, in_reply_to=None, references=None):
    msg = EmailMessage()
    msg["From"] = CONFIG["smtp_from"]
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="southslopenano.com")
    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
    if references:
        msg["References"] = references
    elif in_reply_to:
        msg["References"] = in_reply_to
    msg.set_content(body)

    port = CONFIG.get("smtp_port", 465)
    if port == 465:
        with smtplib.SMTP_SSL(CONFIG["smtp_host"], port) as S:
            S.login(CONFIG["smtp_user"], CONFIG["smtp_pass"])
            S.send_message(msg)
    else:
        with smtplib.SMTP(CONFIG["smtp_host"], port) as S:
            S.starttls(context=ssl.create_default_context())
            S.login(CONFIG["smtp_user"], CONFIG["smtp_pass"])
            S.send_message(msg)


# ----------------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------------

@app.route("/")
def inbox_view():
    try:
        pending = fetch_pending()
    except Exception as e:
        return render_template("inbox.html", pending=[], error=str(e))
    return render_template("inbox.html", pending=pending, error=None)


@app.route("/compose/<uid>")
def compose_view(uid):
    msg = fetch_one(uid)
    if not msg:
        flash(f"Could not load UID {uid}")
        return redirect(url_for("inbox_view"))

    try:
        code = generate_upload_code(msg["from_addr"])
    except Exception as e:
        flash(f"Code generation failed: {e}")
        return redirect(url_for("inbox_view"))

    _subject, body_template = read_reply_template()
    body = body_template.replace("[CODE]", code)

    inbound_subject = (msg["subject"] or "Your Mosaic upload link").strip()
    if re.match(r"(?i)^re:\s", inbound_subject):
        reply_subject = inbound_subject
    else:
        reply_subject = f"Re: {inbound_subject}"

    return render_template(
        "compose.html",
        msg=msg,
        subject=reply_subject,
        body=body,
        code=code,
    )


@app.route("/send/<uid>", methods=["POST"])
def send_view(uid):
    to_addr = request.form["to"].strip()
    subject = request.form["subject"].strip()
    body = request.form["body"]
    in_reply_to = request.form.get("in_reply_to", "").strip() or None
    references = request.form.get("references", "").strip() or None

    try:
        send_reply(to_addr, subject, body, in_reply_to=in_reply_to, references=references)
    except Exception as e:
        flash(f"SMTP send failed: {e}")
        return redirect(url_for("compose_view", uid=uid))

    try:
        mark_handled(uid)
    except Exception as e:
        flash(f"Sent, but mark-as-handled failed: {e}")

    flash(f"Reply sent to {to_addr}.")
    return redirect(url_for("inbox_view"))


@app.route("/ignore/<uid>", methods=["POST"])
def ignore_view(uid):
    try:
        move_to_folder(uid, "Ignored")
        flash("Message moved to Ignored.")
    except Exception as e:
        flash(f"Ignore failed: {e}")
    return redirect(url_for("inbox_view"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=CONFIG.get("port", 5000), debug=False)
