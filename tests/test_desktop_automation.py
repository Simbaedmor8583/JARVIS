from types import SimpleNamespace

import pytest

from config import Config
from skills.desktop_automation import (
    DesktopAdapterRegistry,
    created_files_folder,
    descriptive_filename,
    unique_path,
)


def _ctx():
    return SimpleNamespace(state={}, llm=SimpleNamespace(available=False))


def test_descriptive_filename_rejects_generic_and_invalid_characters():
    name = descriptive_filename("Staff: Training / Proposal", ".docx")
    assert name == "Staff Training Proposal.docx"
    assert name not in {"Document1.docx", "Book1.xlsx", "Presentation1.pptx"}


def test_created_files_use_required_documents_tree(tmp_path, monkeypatch):
    monkeypatch.setattr(Config, "CREATED_FILES_DIR", tmp_path / "Jarvis Created Files")
    folder = created_files_folder("Word")
    assert folder == tmp_path / "Jarvis Created Files" / "Word"
    assert folder.is_dir()


def test_unique_path_never_overwrites_existing_file(tmp_path):
    original = tmp_path / "Proposal.docx"
    original.write_text("existing", encoding="utf-8")
    assert unique_path(original) == tmp_path / "Proposal (2).docx"


def test_desktop_registry_exposes_dedicated_application_adapters():
    registry = DesktopAdapterRegistry(_ctx())
    names = registry.names()
    assert set(("word", "excel", "powerpoint", "outlook", "onenote", "access", "teams", "paint", "edge")) <= set(names)
    for method in (
        "open_word", "create_blank_document", "insert_text", "apply_heading",
        "insert_table", "save_docx", "export_pdf", "close_document",
    ):
        assert callable(getattr(registry.get("word"), method))
    for method in (
        "open_excel", "create_workbook", "select_sheet", "rename_sheet",
        "write_range", "add_formula", "format_range", "create_table",
        "create_chart", "save_xlsx", "export_csv", "close_workbook",
    ):
        assert callable(getattr(registry.get("excel"), method))
    for method in (
        "open_powerpoint", "create_blank_presentation", "add_slide",
        "set_slide_layout", "set_title", "set_body", "add_image",
        "add_notes", "run_slideshow", "save_pptx", "export_pdf",
        "close_presentation",
    ):
        assert callable(getattr(registry.get("powerpoint"), method))


def test_unknown_desktop_adapter_is_rejected():
    with pytest.raises(ValueError, match="Unsupported desktop application adapter"):
        DesktopAdapterRegistry(_ctx()).get("unknown")
