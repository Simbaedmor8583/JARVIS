"""Deterministic planning for compound desktop commands."""
import re


def _intent(skill, **params):
    return {"skill": skill, "params": params}


def plan_command(text):
    command = (text or "").strip()
    low = command.lower()

    live_word = re.search(
        r"open (?:microsoft )?word and (?:create|write|make) (?:a )?(?:full |short )?(?:research )?report (?:about|on) (.+?)(?:[.!]\s*(?:i want to see you type it|do it live|let me watch|show me while you do it|type it in front of me|create it visibly))?[.! ]*$",
        command,
        re.I,
    )
    live_requested = any(phrase in low for phrase in (
        "do it live", "let me watch", "show me while you do it",
        "type it in front of me", "create it visibly", "see you type it",
    ))
    if live_word and live_requested:
        topic = live_word.group(1).strip(" .")
        return [_intent(
            "office_word.create_research_document", topic=topic,
            execution_mode="LIVE_INTERACTIVE", save_after_completion="ASK_USER",
            report_length="short" if "short" in low else "full",
        )]

    research = re.search(
        r"open (?:microsoft )?word and (?:create|write|make) (?:a )?research (?:report|document) (?:about|on) (.+)",
        command,
        re.I,
    )
    if research:
        topic = research.group(1).strip(" .")
        return [
            _intent("app.open_app", target="Microsoft Word"),
            _intent("research.prepare_report", topic=topic),
            _intent("research.gather_report"),
            _intent("research.draft_report"),
            _intent("research.finalize_report"),
            _intent("research.open_report"),
        ]

    youtube = re.search(
        r"open (?:the )?browser,?\s*(?:then\s+)?(?:go|navigate) to youtube,?\s*(?:and\s+)?search (?:youtube )?(?:for )?(.+)",
        command,
        re.I,
    )
    if youtube:
        query = youtube.group(1).strip(" .")
        return [
            _intent("browser.open"),
            _intent("browser.open_site", site="youtube"),
            _intent("browser.search_youtube", query=query),
        ]

    if " and " not in low and "," not in command:
        return []
    return []
