"""
Email — Gmail in the browser (default) with SMTP/IMAP fallback.

Browser mode uses the shared Playwright profile, so a one-time Gmail
login persists across restarts. Every send requires voice confirmation
(unless CONFIRM_SENDS=false in .env).
"""
import re

from config import Config
from brain.prompts import EMAIL_DRAFT_PROMPT, EMAIL_SUMMARY_PROMPT

GMAIL_INBOX = "https://mail.google.com/mail/u/0/#inbox"


# ===========================================================================
# Browser mode helpers
# ===========================================================================
def _open_gmail(ctx):
    """Open (or reuse) the Gmail tab. Returns a Page on the inbox, or None."""
    page = ctx.browser.open_site(GMAIL_INBOX, name="Gmail")
    if page is None:
        return None
    try:
        page.wait_for_selector("tr.zA", timeout=12000)
        return page
    except Exception:
        pass
    if "accounts.google.com" in (page.url or "") or page.query_selector("input[type='email']"):
        ctx.speaker.speak(
            "One-time Gmail login required, sir — you have sixty seconds in "
            "the browser window.")
        try:
            page.wait_for_selector("tr.zA", timeout=60000)
            return page
        except Exception:
            return None
    try:
        page.wait_for_selector("tr.zA", timeout=15000)
        return page
    except Exception:
        return None


def _parse_inbox(page, limit=10):
    """Extract top inbox rows: sender, subject, snippet, unread flag."""
    rows = []
    try:
        for tr in page.query_selector_all("tr.zA")[:limit]:
            cls = (tr.get_attribute("class") or "")
            unread = "zE" in cls.split()
            sender, subject, snippet = "", "", ""
            try:
                el = tr.query_selector("td.yX span.yP, td.yX span.zF, span[email]")
                if el:
                    sender = (el.get_attribute("name")
                              or el.get_attribute("email")
                              or el.inner_text() or "").strip()
            except Exception:
                pass
            try:
                el = tr.query_selector("span.bog")
                if el:
                    subject = (el.inner_text() or "").strip()
            except Exception:
                pass
            try:
                el = tr.query_selector("span.y2")
                if el:
                    snippet = (el.inner_text() or "").strip(" -\n")
            except Exception:
                pass
            rows.append({
                "sender": sender or "Unknown sender",
                "subject": subject or "(no subject)",
                "snippet": snippet,
                "unread": unread,
                "_row": tr,
            })
    except Exception:
        pass
    return rows


def _open_thread(row, page):
    try:
        row["_row"].click()
        page.wait_for_selector("div.a3s, div[role='main']", timeout=12000)
        page.wait_for_timeout(800)
        return True
    except Exception:
        return False


def _extract_thread_text(page):
    parts = []
    try:
        for div in page.query_selector_all("div.a3s"):
            try:
                txt = (div.inner_text() or "").strip()
                if txt:
                    parts.append(txt)
            except Exception:
                continue
    except Exception:
        pass
    return "\n\n".join(parts)[:6000]


def _first(page, selectors, timeout_each=1500):
    for sel in selectors:
        try:
            page.wait_for_selector(sel, timeout=timeout_each)
            el = page.query_selector(sel)
            if el:
                return el
        except Exception:
            continue
    return None


def _fill_compose(page, to, subject, body):
    """Fill the Gmail compose dialog with resilient selectors."""
    compose_btn = _first(page, [
        "div.T-I.T-I-KE",
        "div[role='button'][gh='cm']",
        "div[role='button']:has-text('Compose')",
    ], timeout_each=4000)
    if not compose_btn:
        return False
    try:
        compose_btn.click()
    except Exception:
        return False
    page.wait_for_timeout(1500)

    to_el = _first(page, [
        "div[role='dialog'] div[role='combobox'] input",
        "input[aria-label='To']",
        "textarea[name='to']",
        "div[aria-label='To'][contenteditable='true']",
    ])
    subj_el = _first(page, ["input[name='subjectbox']"])
    body_el = _first(page, [
        "div[aria-label='Message Body']",
        "div[role='textbox'][aria-label*='Body']",
        "div[g_editable='true'][role='textbox']",
    ])
    if not (to_el and subj_el and body_el):
        return False
    try:
        to_el.click()
        to_el.type(to, delay=20)
        page.wait_for_timeout(400)
        page.keyboard.press("Tab")
        subj_el.click()
        subj_el.type(subject, delay=10)
        body_el.click()
        body_el.type(body, delay=2)
        return True
    except Exception:
        return False


def _click_send(page):
    btn = _first(page, [
        "div[role='button'][aria-label*='Send']",
        "div.T-I.J-J5-Ji.aoO",
        "div[role='button']:has-text('Send')",
    ])
    if not btn:
        return False
    try:
        btn.click()
        page.wait_for_timeout(1500)
        return True
    except Exception:
        return False


# ===========================================================================
# SMTP / IMAP fallback
# ===========================================================================
def _smtp_send(to, subject, body):
    import smtplib
    from email.message import EmailMessage
    msg = EmailMessage()
    msg["From"] = Config.EMAIL_ADDRESS
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as smtp:
        smtp.login(Config.EMAIL_ADDRESS, Config.EMAIL_APP_PASSWORD)
        smtp.send_message(msg)


def _imap_top(limit=10):
    import imaplib
    import email
    from email.header import decode_header
    out = []
    with imaplib.IMAP4_SSL("imap.gmail.com", 993) as imap:
        imap.login(Config.EMAIL_ADDRESS, Config.EMAIL_APP_PASSWORD)
        imap.select("INBOX")
        _, data = imap.search(None, "ALL")
        ids = data[0].split()[-limit:]
        for mid in reversed(ids):
            _, msg_data = imap.fetch(mid, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])

            def dec(v):
                if not v:
                    return ""
                parts = decode_header(v)
                return "".join(
                    p.decode(enc or "utf-8", errors="ignore") if isinstance(p, bytes) else p
                    for p, enc in parts
                )
            subject = dec(msg.get("Subject"))
            sender = dec(msg.get("From"))
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        try:
                            body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                            break
                        except Exception:
                            continue
            else:
                try:
                    body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
                except Exception:
                    body = ""
            out.append({"sender": sender, "subject": subject,
                        "snippet": body[:200], "unread": False})
    return out


def _smtp_available():
    return bool(Config.EMAIL_ADDRESS and Config.EMAIL_APP_PASSWORD)


# ===========================================================================
# Actions
# ===========================================================================
def check_email(ctx):
    page = _open_gmail(ctx) if ctx.browser is not None else None
    if page is not None:
        rows = _parse_inbox(page, limit=10)
        if rows:
            ctx.state["email_rows"] = [
                {k: v for k, v in r.items() if not k.startswith("_")} for r in rows
            ]
            unread = [r for r in rows if r["unread"]]
            lines = []
            if unread:
                lines.append(f"You have {len(unread)} unread email"
                             f"{'s' if len(unread) != 1 else ''}, sir.")
            else:
                lines.append("No unread mail, sir. Here is the top of your inbox.")
            for r in rows[:5]:
                marker = "Unread: " if r["unread"] else ""
                lines.append(f"{marker}{r['sender']} — {r['subject']}.")
            return " ".join(lines)

    if _smtp_available():
        try:
            rows = _imap_top(10)
            ctx.state["email_rows"] = rows
            lines = ["Browser Gmail was unavailable, so I checked via IMAP, sir."]
            for r in rows[:5]:
                lines.append(f"{r['sender']} — {r['subject']}.")
            return " ".join(lines)
        except Exception as exc:
            return f"Email check failed on both channels: {exc}."
    return ("I couldn't open Gmail in the browser, and no SMTP credentials "
            "are configured, sir.")


def read_email(target, ctx):
    target = (target or "").strip().lower()
    page = _open_gmail(ctx) if ctx.browser is not None else None
    if page is None:
        return "I couldn't reach the inbox, sir."
    rows = _parse_inbox(page, limit=15)
    chosen = None
    if target:
        for r in rows:
            hay = f"{r['sender']} {r['subject']} {r['snippet']}".lower()
            if target in hay:
                chosen = r
                break
        if chosen is None:
            words = [w for w in target.split() if len(w) > 3]
            for r in rows:
                hay = f"{r['sender']} {r['subject']} {r['snippet']}".lower()
                if any(w in hay for w in words):
                    chosen = r
                    break
    else:
        chosen = rows[0] if rows else None
    if chosen is None:
        return "I couldn't find an email matching that, sir."
    if not _open_thread(chosen, page):
        return "I found the email but couldn't open the thread, sir."
    body = _extract_thread_text(page)
    if not body:
        return "The thread opened, but I couldn't extract its text, sir."
    ctx.state["open_email"] = {"sender": chosen["sender"],
                               "subject": chosen["subject"], "body": body}
    summary = ctx.llm.quick(
        EMAIL_SUMMARY_PROMPT.format(body=body[:4000])) if ctx.llm.available else ""
    if not summary:
        summary = f"From {chosen['sender']}, subject {chosen['subject']}. " + body[:400]
    return summary


def _parse_draft(text):
    subject, body = "", ""
    m = re.search(r"SUBJECT:\s*(.+)", text)
    if m:
        subject = m.group(1).strip()
    m = re.search(r"BODY:\s*(.*)", text, flags=re.DOTALL)
    if m:
        body = m.group(1).strip()
    if not body:
        body = text
    return subject or "Message from JARVIS", body


def compose_email(to, topic, ctx, reply_context=None):
    to = (to or "").strip()
    topic = (topic or "").strip()
    if not to and not reply_context:
        return "Who should I write to, sir?"
    extra = ""
    if reply_context:
        extra = (f"This is a reply. Original sender: {reply_context.get('sender')}. "
                 f"Original subject: {reply_context.get('subject')}. "
                 f"Original body excerpt: {reply_context.get('body', '')[:1500]}")
    draft_text = ctx.llm.quick(
        EMAIL_DRAFT_PROMPT.format(to=to or reply_context.get("sender", ""),
                                  topic=topic or "Reply", extra=extra),
        max_tokens=1200,
    ) if ctx.llm.available else ""
    if not draft_text:
        return "My drafting service is unavailable, sir. Check the OpenRouter key."
    subject, body = _parse_draft(draft_text)
    if reply_context and not subject.lower().startswith("re:"):
        subject = "Re: " + reply_context.get("subject", subject)

    print("\n----- EMAIL DRAFT -----", flush=True)
    print(f"To: {to or reply_context.get('sender', '')}", flush=True)
    print(f"Subject: {subject}", flush=True)
    print(body, flush=True)
    print("-----------------------\n", flush=True)

    def _send():
        page = _open_gmail(ctx) if ctx.browser is not None else None
        if page is not None:
            if reply_context:
                btn = _first(page, [
                    "div[role='button'][aria-label*='Reply']",
                    "span[role='link']:has-text('Reply')",
                    "div[role='button']:has-text('Reply')",
                ])
                if btn:
                    try:
                        btn.click()
                        page.wait_for_timeout(1200)
                        body_el = _first(page, [
                            "div[aria-label='Message Body']",
                            "div[g_editable='true'][role='textbox']",
                        ])
                        if body_el:
                            body_el.click()
                            body_el.type(body, delay=2)
                            if _click_send(page):
                                return "Reply sent, sir."
                    except Exception:
                        pass
            else:
                if _fill_compose(page, to, subject, body) and _click_send(page):
                    return "Sent, sir."
        if _smtp_available():
            try:
                _smtp_send(to or reply_context.get("sender", ""), subject, body)
                return "Sent via SMTP, sir."
            except Exception as exc:
                return f"Both Gmail UI and SMTP failed: {exc}."
        return ("The Gmail interface defeated me, and no SMTP fallback is "
                "configured, sir.")

    if Config.CONFIRM_SENDS:
        ctx.speaker.speak(
            f"Draft ready for {to or reply_context.get('sender', '')}. "
            f"Subject: {subject}. Shall I send it? Say yes or no.")
        ctx.pending = {
            "kind": "confirm",
            "prompt": "send email",
            "on_yes": _send,
            "on_no": lambda: "Discarded, sir.",
        }
        return None
    return _send()


def reply_last(ctx):
    current = ctx.state.get("open_email")
    if not current:
        return "I don't have an open email to reply to, sir. Ask me to read one first."
    return compose_email(current.get("sender", ""), "Reply", ctx,
                         reply_context=current)


# ===========================================================================
# Skill dispatch entry
# ===========================================================================
def handle(intent, ctx):
    skill = intent.get("skill")
    params = intent.get("params", {}) or {}
    if skill == "email.check":
        return check_email(ctx)
    if skill == "email.read":
        return read_email(params.get("target", ""), ctx)
    if skill == "email.compose":
        return compose_email(params.get("to", ""), params.get("topic", ""), ctx)
    if skill == "email.reply":
        return reply_last(ctx)
    return None
