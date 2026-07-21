"""Reusable website adapters built on verified Playwright operations."""
from __future__ import annotations

import re
from urllib.parse import quote_plus


class WebsiteAdapter:
    name = ""
    domains = ()

    def __init__(self, automation):
        self.automation = automation

    def open(self):
        return self.automation.open_website(self.name)

    def page(self):
        page = self.automation._active_page()
        if page is None or not self.automation.verify_domain(page, self.domains):
            return None
        return page

    def require_page(self):
        page = self.page()
        if page is None:
            raise RuntimeError(f"The active tab is not verified for {self.name}")
        return page


class GoogleAdapter(WebsiteAdapter):
    name = "google"
    domains = ("google.com",)

    def open_google(self):
        return self.open()

    def search_google(self, query):
        return self.automation.search_web(query)

    def read_results(self):
        return self.automation.read_page()

    def open_result(self, index=0):
        page = self.require_page()
        links = page.locator("a:has(h3)")
        links.nth(max(0, int(index))).click(timeout=10000)
        page.wait_for_load_state("domcontentloaded", timeout=30000)
        return self.automation._result("success", "open_result", "Opened the selected Google result.", page)

    def filter_results(self, phrase):
        return self.automation.find_on_page(phrase)


class YouTubeAdapter(WebsiteAdapter):
    name = "youtube"
    domains = ("youtube.com", "youtu.be")

    def open_youtube(self):
        return self.open()

    def search_videos(self, query):
        return self.automation.search_youtube(query)

    def open_video(self, index=0):
        page = self.require_page()
        page.locator("a#video-title").nth(max(0, int(index))).click(timeout=15000)
        page.wait_for_load_state("domcontentloaded", timeout=30000)
        return self.automation._result("success", "open_video", "Opened the selected YouTube video.", page)

    def play_video(self):
        return self.automation.video_control("play")

    def pause_video(self):
        return self.automation.video_control("pause")

    def enable_captions(self):
        page = self.require_page()
        page.locator("button.ytp-subtitles-button").click(timeout=10000)
        return self.automation._result("success", "enable_captions", "YouTube captions toggled.", page)

    def open_transcript(self):
        page = self.require_page()
        page.get_by_role("button", name=re.compile("transcript", re.I)).click(timeout=10000)
        return self.automation._result("success", "open_transcript", "YouTube transcript opened.", page)

    def search_channel(self, query):
        return self.search_videos(query)


class GmailAdapter(WebsiteAdapter):
    name = "gmail"
    domains = ("mail.google.com",)

    def open_gmail(self):
        return self.open()

    def search_email(self, query):
        page = self.require_page()
        box = page.locator("input[placeholder*='Search'], input[aria-label*='Search']").first
        box.fill(str(query))
        box.press("Enter")
        page.wait_for_timeout(1500)
        return self.automation._result("success", "search_email", "Gmail search results are visible.", page)

    def open_email(self, index=0):
        page = self.require_page()
        page.locator("tr[role=main]", has_text="").nth(max(0, int(index))).click(timeout=10000)
        return self.automation._result("success", "open_email", "Opened the selected email.", page)

    def read_thread(self):
        return self.automation.read_page()

    def create_draft(self, to="", subject="", body=""):
        page = self.require_page()
        page.get_by_text(re.compile(r"^compose$", re.I)).click(timeout=10000)
        if to:
            page.locator("input[name=to], input[aria-label^='To']").first.fill(str(to))
        if subject:
            page.locator("input[name=subjectbox]").fill(str(subject))
        if body:
            page.locator("div[aria-label='Message Body'], div[role=textbox]").last.fill(str(body))
        return self.automation._result("success", "create_draft", "Email draft prepared and left unsent.", page)

    def reply(self, body):
        page = self.require_page()
        page.get_by_text(re.compile(r"^reply$", re.I)).last.click(timeout=10000)
        page.locator("div[role=textbox]").last.fill(str(body))
        return self.automation._result("success", "reply", "Reply draft prepared and left unsent.", page)

    def add_attachment(self, path):
        return self.automation.upload(path)

    def send_after_approval(self):
        return self.automation.submit_form("div[role=button][data-tooltip*='Send'], div[role=button][aria-label*='Send']")


class GoogleDriveAdapter(WebsiteAdapter):
    name = "google drive"
    domains = ("drive.google.com",)

    def open_drive(self):
        return self.open()

    def search_files(self, query):
        page = self.require_page()
        box = page.locator("input[placeholder*='Search'], input[aria-label*='Search']").first
        box.fill(str(query))
        box.press("Enter")
        page.wait_for_timeout(1200)
        return self.automation._result("success", "search_files", "Google Drive search results are visible.", page)

    def open_file(self, name):
        page = self.require_page()
        page.get_by_text(str(name), exact=False).first.dblclick(timeout=10000)
        return self.automation._result("success", "open_file", f"Opened {name} in Google Drive.", page)

    def upload_file(self, path):
        return self.automation.upload(path)

    def download_file(self, name):
        return self.automation.download(name)

    def create_folder(self, name):
        page = self.require_page()
        page.get_by_text(re.compile(r"^new$", re.I)).click(timeout=10000)
        page.get_by_text(re.compile(r"^new folder$", re.I)).click(timeout=10000)
        dialog = page.get_by_role("dialog")
        dialog.locator("input").fill(str(name))
        dialog.get_by_role("button", name=re.compile("create", re.I)).click()
        return self.automation._result("success", "create_folder", f"Created Drive folder {name}.", page)

    def move_file(self, name):
        raise RuntimeError("Move requires a verified destination folder selection")

    def share_after_approval(self):
        return self.automation.submit_form("button[aria-label*='Share'], div[role=button][aria-label*='Share']")


class GoogleDocsAdapter(WebsiteAdapter):
    name = "google docs"
    domains = ("docs.google.com",)

    def create_blank(self, title="JARVIS Document", text=""):
        result = self.automation.new_tab("https://docs.google.com/document/u/0/create")
        page = self.require_page()
        page.wait_for_timeout(2000)
        try:
            page.locator("input.docs-title-input").fill(str(title))
        except Exception:
            pass
        if text:
            page.keyboard.type(str(text), delay=10)
        return result

    def type_text(self, text):
        page = self.require_page()
        page.keyboard.type(str(text), delay=10)
        return self.automation._result("success", "type_text", "Text entered in Google Docs.", page)


class GoogleSheetsAdapter(WebsiteAdapter):
    name = "google sheets"
    domains = ("docs.google.com",)

    def create_blank(self, title="JARVIS Spreadsheet"):
        result = self.automation.new_tab("https://docs.google.com/spreadsheets/u/0/create")
        page = self.require_page()
        page.wait_for_timeout(2000)
        try:
            page.locator("input.docs-title-input").fill(str(title))
        except Exception:
            pass
        return result

    def create_monthly_budget(self):
        result = self.create_blank("Monthly Budget")
        page = self.require_page()
        page.keyboard.type("Category\tBudget\tActual\tDifference\tNotes\nHousing\t0\t0\t=B2-C2\nUtilities\t0\t0\t=B3-C3", delay=8)
        return result


class GoogleSlidesAdapter(WebsiteAdapter):
    name = "google slides"
    domains = ("docs.google.com",)

    def create_blank(self, title="JARVIS Presentation"):
        result = self.automation.new_tab("https://docs.google.com/presentation/u/0/create")
        page = self.require_page()
        page.wait_for_timeout(2000)
        try:
            page.locator("input.docs-title-input").fill(str(title))
        except Exception:
            pass
        return result

    def create_presentation(self, title="JARVIS Presentation", slides=10):
        result = self.create_blank(title)
        page = self.require_page()
        count = max(1, min(int(slides or 10), 20))
        page.keyboard.type(str(title), delay=10)
        for index in range(2, count + 1):
            page.keyboard.press("Control+m")
            page.keyboard.type(f"Slide {index}: {title}", delay=8)
        return result


class StripeAdapter(WebsiteAdapter):
    name = "stripe"
    domains = ("dashboard.stripe.com",)

    def open_dashboard(self):
        return self.open()

    def search_payment(self, query):
        page = self.require_page()
        page.locator("input[type=search], input[placeholder*='Search']").first.fill(str(query))
        page.keyboard.press("Enter")
        return self.automation._result("success", "search_payment", "Stripe payment search results are visible.", page)

    def search_customer(self, query):
        return self.search_payment(query)

    def open_invoice(self, query):
        return self.search_payment(query)

    def download_report(self, name="Download"):
        return self.automation.download(name)

    def refund_after_approval(self):
        return self.automation.submit_form("button:has-text('Refund'), [role=button]:has-text('Refund')")


class GitHubAdapter(WebsiteAdapter):
    name = "github"
    domains = ("github.com",)

    def open_github(self):
        return self.open()

    def search_repository(self, query):
        page = self.require_page()
        page.goto("https://github.com/search?q=" + quote_plus(str(query)) + "&type=repositories", wait_until="domcontentloaded")
        return self.automation._result("success", "search_repository", "GitHub repository results are visible.", page)

    def open_issue(self, number):
        return self.automation.find_on_page(f"#{number}")

    def open_pull_request(self, number):
        return self.automation.find_on_page(f"#{number}")

    def read_file(self):
        return self.automation.read_page()

    def download_release(self, name="Assets"):
        return self.automation.download(name)


class WebsiteAdapterRegistry:
    def __init__(self, automation):
        self._adapters = {
            "google": GoogleAdapter(automation),
            "youtube": YouTubeAdapter(automation),
            "gmail": GmailAdapter(automation),
            "google drive": GoogleDriveAdapter(automation),
            "google docs": GoogleDocsAdapter(automation),
            "google sheets": GoogleSheetsAdapter(automation),
            "google slides": GoogleSlidesAdapter(automation),
            "stripe": StripeAdapter(automation),
            "github": GitHubAdapter(automation),
        }

    def get(self, name):
        key = str(name or "").lower().strip()
        if key not in self._adapters:
            raise ValueError(f"Unknown website adapter: {name}")
        return self._adapters[key]

    def names(self):
        return tuple(sorted(self._adapters))


class WebsiteAutomationService:
    def __init__(self, automation):
        self.automation = automation
        self.adapters = WebsiteAdapterRegistry(automation)

    def execute(self, intent):
        skill = intent.get("skill", "")
        params = dict(intent.get("params", {}) or {})
        intent_group = params.pop("intent_group", skill)
        operations = {
            "website.gmail_search": lambda: self.adapters.get("gmail").search_email(params.get("query", "")),
            "website.gmail_open_latest": lambda: self.adapters.get("gmail").open_email(0),
            "website.gmail_reply_draft": lambda: self.adapters.get("gmail").reply(params.get("body", "")),
            "website.drive_search": lambda: self.adapters.get("google drive").search_files(params.get("query", "")),
            "website.drive_show_location": lambda: self.automation.read_page(),
            "website.stripe_search_payment": lambda: self.adapters.get("stripe").search_payment(params.get("query", "")),
        }
        operation = operations.get(skill)
        if operation is None:
            raise ValueError(f"Unsupported website automation intent: {skill}")
        result = operation()
        self.automation.logger.write(
            result, intent=intent_group,
            command=self.automation.ctx.state.get("last_command_text", ""),
        )
        return result.message
