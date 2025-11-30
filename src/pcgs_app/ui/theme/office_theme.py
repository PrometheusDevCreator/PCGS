"""
Office Template Theme Helpers

Maps theme tokens into PPTX/DOCX template placeholders so exports stay in sync
with the UI branding choices.
"""

from typing import Dict

from . import tokens


def get_office_theme() -> Dict[str, str]:
    """
    Return a minimal mapping of theme tokens to Office template placeholders.
    """

    # TODO: Replace with structured template metadata referencing actual file
    # manifests and placeholder keys.
    return {
        "title_font": tokens.FONTS["heading"],
        "body_font": tokens.FONTS["body"],
        "primary_color": tokens.COLORS["primary"],
    }


