"""
Shared Chrome Components

Reusable header, footer, and AI console renderers for consistent styling
across all PCGS V2 tabs.
"""

import html
from datetime import datetime
from typing import Callable, Dict, List, Optional, Tuple

import streamlit as st

from pcgs_app.logic.lexicon import Lex
from pcgs_app.ui.theme.tokens import ICONS


# ============================================================================
# Constants
# ============================================================================

CURRENT_USER = "Matthew Dodds"
START_DATE = "24/11/25"
PROGRAM_STATUS = "IN DEVELOPMENT"
APPROVED_FOR_USE = "N"
PKE_ICON = ICONS.get("pke", "🔥")
HISTORY_LIMIT = 60


# ============================================================================
# Header Components
# ============================================================================

def render_header_band(
    page_title: Optional[str] = None,
    buttons: Optional[List[Tuple[str, str, Callable[[], None]]]] = None,
    horizontal_buttons: bool = True,
) -> None:
    """
    Render the top status band with course info and action buttons.
    
    Args:
        page_title: Optional page-specific title (e.g. "SCALAR MANAGER")
        buttons: List of (label, tone, handler) tuples for action buttons
        horizontal_buttons: If True, buttons are laid out horizontally; else vertically
    """
    st.markdown("<div class='pcgs-status-band'>", unsafe_allow_html=True)
    st.markdown("<div class='pcgs-status-band__left'>", unsafe_allow_html=True)
    _render_header_status(page_title)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if buttons:
        st.markdown("<div class='pcgs-status-band__right'>", unsafe_allow_html=True)
        _render_action_buttons(buttons, horizontal=horizontal_buttons)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def _render_header_status(page_title: Optional[str] = None) -> None:
    """Render the status information cluster in the header."""
    now_str = datetime.now().strftime("%d %b %Y %H:%M")
    
    # Get course info from session state if available
    course_info = st.session_state.get("pcgs_course_info", {})
    title = course_info.get(Lex.C_NAME, "") or "UNSPECIFIED"
    duration = course_info.get(Lex.C_DURATION, "") or "N/A"
    level = course_info.get(Lex.C_LEVEL, "") or "UNSPECIFIED"
    thematic = course_info.get(Lex.C_THEME, "") or "UNSPECIFIED"
    
    page_title_html = ""
    if page_title:
        page_title_html = f'<div class="pcgs-header-status__page-title">{html.escape(page_title)}</div>'
    
    status_html = f"""
    <div class="pcgs-header-status">
        <div class="pcgs-header-status__title">PROMETHEUS COURSE GENERATION SYSTEM 2.0</div>
        {page_title_html}
        <div class="pcgs-header-status__timestamp">{now_str}</div>
        <div class="pcgs-header-status__metrics">
            <span>Course Loaded · {html.escape(str(title))}</span>
            <span>Duration · {html.escape(str(duration))}</span>
            <span>Level · {html.escape(str(level))}</span>
            <span>Thematic · {html.escape(str(thematic))}</span>
        </div>
    </div>
    """
    st.markdown(status_html, unsafe_allow_html=True)


def _render_action_buttons(
    buttons: List[Tuple[str, str, Callable[[], None]]],
    horizontal: bool = True,
) -> None:
    """
    Render action buttons.
    
    Args:
        buttons: List of (label, tone, handler) tuples
        horizontal: If True, lay out horizontally; else vertically
    """
    wrapper_class = "pcgs-top-buttons--horizontal" if horizontal else "pcgs-top-buttons"
    st.markdown(f"<div class='{wrapper_class}'>", unsafe_allow_html=True)
    
    for label, tone, handler in buttons:
        disabled = tone == "disabled"
        btn_class = f"pcgs-pill-button pcgs-pill-button--{tone}"
        st.markdown(f"<div class='{btn_class}'>", unsafe_allow_html=True)
        key = f"pcgs_ctrl_{label.lower().replace('/', '_').replace(' ', '_')}"
        if st.button(label, key=key, disabled=disabled):
            if handler and not disabled:
                handler()
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# Footer Component
# ============================================================================

def render_footer(progress_percent: int = 0) -> None:
    """
    Render the bottom status strip.
    
    Args:
        progress_percent: Progress percentage (0-100)
    """
    st.markdown("<div class='pcgs-footer'>", unsafe_allow_html=True)
    st.markdown(f"<div><strong>Owner:</strong> {CURRENT_USER.upper()}</div>", unsafe_allow_html=True)
    st.markdown(f"<div><strong>Start Date:</strong> {START_DATE}</div>", unsafe_allow_html=True)
    st.markdown(f"<div><strong>Status:</strong> {PROGRAM_STATUS}</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div><strong>Progress:</strong> {progress_percent}%"
        f"<div class='pcgs-progress'><div class='pcgs-progress__value' style='width: {progress_percent}%;'></div></div></div>",
        unsafe_allow_html=True,
    )
    st.markdown(f"<div><strong>Approved for Use Y/N:</strong> {APPROVED_FOR_USE}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# AI Console Component
# ============================================================================

def render_ai_console(
    history_key: str = "pcgs_ai_history",
    input_key: str = "pcgs_ai_input",
    on_submit: Optional[Callable[[], None]] = None,
    console_title: str = "PROMETHEUS AI",
    placeholder_text: str = "Type your request and press Enter…",
    default_message: str = "PROMETHEUS Knowledge Engine calibrated. Awaiting trigger.",
) -> None:
    """
    Render the gold PKE AI console band.
    
    Args:
        history_key: Session state key for chat history
        input_key: Session state key for input field
        on_submit: Optional callback when user submits input
        console_title: Title shown at top of console
        placeholder_text: Placeholder for input field
        default_message: Default PKE message if history is empty
    """
    active = st.session_state.get("pcgs_ai_mode", "idle") != "idle"
    band_class = "pcgs-ai-band pcgs-ai-band--active" if active else "pcgs-ai-band"
    
    st.markdown(f"<div class='{band_class}'>", unsafe_allow_html=True)
    st.markdown(f"<div class='pcgs-ai-band__header'>{html.escape(console_title)}</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='pcgs-ai-band__feed'>", unsafe_allow_html=True)
    
    history = st.session_state.get(history_key, [("PKE", default_message)])
    for speaker, text in history[-HISTORY_LIMIT:]:
        prefix = "[PKE]" if speaker == "PKE" else "&gt;"
        st.markdown(
            f"<div class='pcgs-ai-band__line'><span class='pcgs-ai-band__speaker'>{prefix}</span>{html.escape(text)}</div>",
            unsafe_allow_html=True,
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='pcgs-ai-band__prompt'>PROMPT<span class='pcgs-ai-band__caret'></span></div>", unsafe_allow_html=True)
    
    st.text_input(
        "PKE Input",
        key=input_key,
        label_visibility="collapsed",
        placeholder=placeholder_text,
        on_change=on_submit,
    )
    
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# Navigation Helper
# ============================================================================

def navigate_to_tab(tab_id: str) -> None:
    """
    Set session state to navigate to a different tab.
    
    The main shell (main_shell.py) reads this on the next rerun.
    """
    st.session_state["pcgs_navigate_to_tab"] = tab_id


# ============================================================================
# Shared Styles Injection
# ============================================================================

def inject_shared_chrome_styles() -> None:
    """Inject additional CSS for shared chrome components."""
    css = """
    <style>
    /* Horizontal button layout for top bar */
    .pcgs-top-buttons--horizontal {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 0.65rem;
        flex-wrap: wrap;
        justify-content: flex-end;
    }
    
    .pcgs-top-buttons--horizontal .pcgs-pill-button {
        min-width: 100px;
        flex: 0 0 auto;
    }
    
    .pcgs-top-buttons--horizontal .pcgs-pill-button button {
        height: 40px;
        padding: 0 1.2rem;
        font-size: 0.8rem;
    }
    
    /* Page title styling (for manager pages) */
    .pcgs-header-status__page-title {
        color: #2CF0FF;
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: 0.2em;
        margin-top: 0.3rem;
        text-transform: uppercase;
    }
    
    /* AI console header */
    .pcgs-ai-band__header {
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.15em;
        color: rgba(31, 19, 2, 0.75);
        margin-bottom: 0.5rem;
        text-transform: uppercase;
    }
    
    /* Disabled pill button */
    .pcgs-pill-button--disabled {
        opacity: 0.4;
        pointer-events: none;
    }
    
    .pcgs-pill-button--disabled button {
        cursor: not-allowed !important;
        color: rgba(255, 255, 255, 0.5) !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

