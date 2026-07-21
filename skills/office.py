"""Office document compatibility facade."""
from skills.excel_skill import create_spreadsheet as create_workbook
from skills.ppt_skill import create_presentation
from skills.word_skill import continue_document, write_document

__all__ = [
    "write_document",
    "continue_document",
    "create_workbook",
    "create_presentation",
]
