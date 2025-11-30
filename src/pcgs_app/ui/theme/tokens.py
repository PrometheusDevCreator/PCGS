"""
Theme Tokens

Defines the design tokens (colours, fonts, spacing, icons) that will drive both
the Streamlit UI and Office exports.
"""

from dataclasses import dataclass

# TODO: Populate with brand-approved palette and typography from governance docs.

COLORS = {
    "primary": "#2CF0FF",
    "secondary": "#11A7C7",
    "accent": "#FFB347",
}

FONTS = {
    "heading": "IBM Plex Sans",
    "body": "Inter",
    "mono": "IBM Plex Mono",
}

SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 16,
    "lg": 24,
    "xl": 32,
}

ICONS = {
    "pke": "🔥",
}


@dataclass(frozen=True)
class ThemeTokens:
    """
    Container for Streamlit + Office theme values.
    """

    bg_main: str
    bg_panel: str
    bg_panel_subtle: str
    accent_primary: str
    accent_secondary: str
    accent_warning: str
    accent_error: str
    accent_success: str
    text_primary: str
    text_muted: str
    text_ai: str
    glow_ai: str
    glow_progress: str
    font_heading: str = FONTS["heading"]
    font_body: str = FONTS["body"]
    font_mono: str = FONTS["mono"]


def get_default_tokens() -> ThemeTokens:
    """
    Return the default neon/sci-fi inspired token set.
    """

    return ThemeTokens(
        bg_main="#01030B",
        bg_panel="#080F1F",
        bg_panel_subtle="#040812",
        accent_primary="#2CF0FF",
        accent_secondary="#0F8FB5",
        accent_warning="#F7E374",
        accent_error="#FF4D6D",
        accent_success="#62FFB7",
        text_primary="#E9F6FF",
        text_muted="#6FA8CE",
        text_ai="#1F1302",
        glow_ai="#FFB347",
        glow_progress="#7CFFAF",
    )

