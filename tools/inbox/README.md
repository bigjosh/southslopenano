# Mosaic inbox

Local Flask app that:

1. Reads unread mail from the `mosaic@southslopenano.com` IMAP inbox.
2. Lists each pending request with from/to/subject/body.
3. On "Reply with link" — calls the upload-server's `generate-code` API
   (with the sender's email as `backer-id`, notes `Mosaic`), prefills the
   reply body from `copy/emails/upload-link-reply.md` with `[CODE]`
   substituted, and lets you edit before sending.
4. On Send — fires the reply via SMTP, marks the inbound as Seen, copies
   it to a `Replied` IMAP folder, deletes the original from INBOX,
   expunges.

Local-only. Binds to `127.0.0.1`. Don't expose this to the network.

## Install & run

```bash
cd tools/inbox
pip install -r requirements.txt
cp config.example.json config.json
# edit config.json with real values (imap pass, smtp pass, admin_id)
python app.py
```

Then open <http://127.0.0.1:5000>.

## Config fields

| key | what |
|---|---|
| `imap_host`, `imap_port`, `imap_user`, `imap_pass` | IMAP creds. SSL on 993 expected. |
| `smtp_host`, `smtp_port`, `smtp_user`, `smtp_pass` | SMTP creds. SSL on 465 by default; set port `587` to use STARTTLS instead. |
| `smtp_from` | "From" header on outbound replies. E.g. `Mosaic <mosaic@southslopenano.com>` |
| `admin_id` | The admin token recognized by `app.py` on the upload server. |
| `generate_code_url` | The full URL of `upload-server/app.py`. Default: `https://mosaic.southslopenano.com/upload/cgi-bin/app.py` |
| `port` | Local port. Default 5000. |

`config.json` is gitignored. Don't commit it.

## Notes

- **Template lives in the campaign repo.** The reply body is read from
  `copy/emails/upload-link-reply.md` *at request time*. Edit that file
  and the next reply uses the new version. The Subject is read from the
  `## Subject` section; the Body from `## Body`. Both as Markdown
  blockquotes.
- **One code per click.** Hitting "Reply with link" generates a fresh
  code on every load — even if you don't end up sending. Backing out
  leaves a dangling code on the upload server. Cheap; safer than
  generating only on send (you'd never see the URL before sending).
- **Replied folder.** The first send creates the `Replied` IMAP folder
  automatically if it doesn't exist.
- **Threading.** The reply sets `In-Reply-To` and `References` so it
  shows up in the user's email client as a reply to their original
  message, not a fresh thread.
