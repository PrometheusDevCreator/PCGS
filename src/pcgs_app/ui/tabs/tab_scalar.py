"""
Scalar Manager V2 Tab

Implements the Prometheus V2 Scalar Manager with:
- Excel import from template
- Manual add/edit/delete/reorder
- Bloom's verb validation for CLOs
- Two-column layout matching Figma design
- Global elements (top bar, AI console, bottom strip)

Layout Structure (Template B - Manager 2-Column):
- Left column (~28-30%): SCALAR CONTROL panel
- Right column (~70-72%): SCALAR GRID panel with 6 columns
"""

import copy
import html
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

import streamlit as st

from pcgs_app.core.scalar_models import ScalarLevel, ScalarEntry, BLOOMS_VERBS
from pcgs_app.logic.lexicon import Lex
from pcgs_app.services import scalar_service
from pcgs_app.ui.theme.streamlit_theme import apply_base_theme
from pcgs_app.ui.theme.tokens import ICONS, get_default_tokens
from pcgs_app.ui.widgets.status_lights import render_status_dot


# ============================================================================
# Constants
# ============================================================================

CURRENT_USER = "Matthew Dodds"
START_DATE = "24/11/25"
PROGRAM_STATUS = "IN DEVELOPMENT"
APPROVED_FOR_USE = "N"

PKE_ICON = ICONS.get("pke", "🔥")

# Column configuration for the scalar grid
SCALAR_COLUMNS = [
    {"level": ScalarLevel.CLO, "label": "CLOs", "key": "clo"},
    {"level": ScalarLevel.TOPIC, "label": "Topics", "key": "topic"},
    {"level": ScalarLevel.SUBTOPIC, "label": "Subtopics", "key": "subtopic"},
    {"level": ScalarLevel.LESSON, "label": "Lessons", "key": "lesson"},
    {"level": ScalarLevel.PERFORMANCE_CRITERIA, "label": "Perf. Criteria", "key": "pc"},
    {"level": None, "label": "Reserved", "key": "reserved"},
]

# Edit tool buttons
EDIT_TOOLS = ["SELECT", "REORDER", "BULK EDIT", "DELETE"]

# Navigation state keys
NAV_STATE_KEY = "pcgs_current_tab"
SCALAR_EDIT_MODE_KEY = "pcgs_scalar_edit_mode"
SCALAR_EDITING_ENTRY_KEY = "pcgs_scalar_editing_entry"


# ============================================================================
# Main Render Function
# ============================================================================

def render_tab_scalar() -> None:
    """
    Render the Scalar Manager V2 tab.
    
    This is the main entry point called by app_root.py.
    """
    apply_base_theme(get_default_tokens())
    _init_state()
    
    st.markdown("<div class='pcgs-root pcgs-scalar-root'>", unsafe_allow_html=True)
    _render_region("pcgs-region-status", _render_header)
    _render_region("pcgs-region-scalar-left", _render_control_panel)
    _render_region("pcgs-region-scalar-right", _render_grid_panel)
    _render_region("pcgs-region-ai", _render_ai_band)
    _render_region("pcgs-region-footer", _render_footer)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Inject Scalar Manager specific styles
    _inject_scalar_styles()


def _render_region(region_class: str, renderer: Callable[[], None]) -> None:
    """Render a UI region with wrapper div."""
    with st.container():
        st.markdown(f"<div class='{region_class}'>", unsafe_allow_html=True)
        renderer()
        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# State Management
# ============================================================================

def _init_state() -> None:
    """Initialize scalar tab state."""
    scalar_service.init_scalar_state()
    
    # Edit mode state
    if SCALAR_EDIT_MODE_KEY not in st.session_state:
        st.session_state[SCALAR_EDIT_MODE_KEY] = None  # None, "select", "reorder", "bulk_edit", "delete"
    if SCALAR_EDITING_ENTRY_KEY not in st.session_state:
        st.session_state[SCALAR_EDITING_ENTRY_KEY] = None  # (level, serial) tuple when editing


def _set_edit_mode(mode: Optional[str]) -> None:
    """Set the current edit mode."""
    st.session_state[SCALAR_EDIT_MODE_KEY] = mode
    if mode is None:
        st.session_state[SCALAR_EDITING_ENTRY_KEY] = None


def _get_edit_mode() -> Optional[str]:
    """Get the current edit mode."""
    return st.session_state.get(SCALAR_EDIT_MODE_KEY)


def _start_editing(level: ScalarLevel, serial: str) -> None:
    """Start editing a specific entry."""
    st.session_state[SCALAR_EDITING_ENTRY_KEY] = (level, serial)


def _stop_editing() -> None:
    """Stop editing."""
    st.session_state[SCALAR_EDITING_ENTRY_KEY] = None


def _is_editing(level: ScalarLevel, serial: str) -> bool:
    """Check if a specific entry is being edited."""
    editing = st.session_state.get(SCALAR_EDITING_ENTRY_KEY)
    return editing == (level, serial)


# ============================================================================
# Header Section
# ============================================================================

def _render_header() -> None:
    """Render the header with status info and action buttons."""
    st.markdown("<div class='pcgs-status-band'>", unsafe_allow_html=True)
    st.markdown("<div class='pcgs-status-band__left'>", unsafe_allow_html=True)
    _render_header_status()
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='pcgs-status-band__right'>", unsafe_allow_html=True)
    _render_top_buttons()
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def _render_header_status() -> None:
    """Render the status information in header."""
    now_str = datetime.now().strftime("%d %b %Y %H:%M")
    
    # Get course info from session state if available
    course_info = st.session_state.get("pcgs_course_info", {})
    title = course_info.get(Lex.C_NAME, "") or "UNSPECIFIED"
    duration = course_info.get(Lex.C_DURATION, "") or "N/A"
    level = course_info.get(Lex.C_LEVEL, "") or "UNSPECIFIED"
    thematic = course_info.get(Lex.C_THEME, "") or "UNSPECIFIED"
    
    status_html = f"""
    <div class="pcgs-header-status">
        <div class="pcgs-header-status__title">PROMETHEUS COURSE GENERATION SYSTEM 2.0</div>
        <div class="pcgs-header-status__page-title">SCALAR MANAGER</div>
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


def _render_top_buttons() -> None:
    """Render top action buttons (LOAD disabled, SAVE, DELETE disabled, CLEAR)."""
    st.markdown("<div class='pcgs-top-buttons'>", unsafe_allow_html=True)
    
    # LOAD - disabled on Scalar Manager
    st.markdown("<div class='pcgs-pill-button pcgs-pill-button--disabled'>", unsafe_allow_html=True)
    st.button("LOAD", key="pcgs_scalar_load", disabled=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # SAVE - active
    st.markdown("<div class='pcgs-pill-button pcgs-pill-button--primary'>", unsafe_allow_html=True)
    if st.button("SAVE", key="pcgs_scalar_save"):
        _handle_save()
    st.markdown("</div>", unsafe_allow_html=True)
    
    # DELETE - disabled on Scalar Manager
    st.markdown("<div class='pcgs-pill-button pcgs-pill-button--disabled'>", unsafe_allow_html=True)
    st.button("DELETE", key="pcgs_scalar_delete_btn", disabled=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # CLEAR - active
    st.markdown("<div class='pcgs-pill-button pcgs-pill-button--neutral'>", unsafe_allow_html=True)
    if st.button("CLEAR", key="pcgs_scalar_clear"):
        _handle_clear()
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def _handle_save() -> None:
    """Handle save button click."""
    # Get current course scalar
    course_scalar = st.session_state.get("pcgs_course_scalar", [])
    # Save and update
    new_scalar = scalar_service.save_scalar_to_course(course_scalar)
    st.session_state["pcgs_course_scalar"] = new_scalar
    st.success("Scalar saved successfully.")


def _handle_clear() -> None:
    """Handle clear button click."""
    scalar_service.clear_scalar()
    st.info("Scalar cleared. Remember to SAVE to confirm.")


# ============================================================================
# Left Panel - Scalar Control
# ============================================================================

def _render_control_panel() -> None:
    """Render the left SCALAR CONTROL panel."""
    classes = "pcgs-panel pcgs-panel--scalar-control"
    
    st.markdown(f"<div class='{classes}'>", unsafe_allow_html=True)
    st.markdown(
        "<div class='pcgs-panel__header'><div class='pcgs-panel__title'>SCALAR CONTROL</div></div>",
        unsafe_allow_html=True,
    )
    
    # A) Import Scalar Section
    _render_import_section()
    
    # B) Edit Tools Section
    _render_edit_tools()
    
    # C) Master PKE Control
    _render_pke_control()
    
    # D) Navigation Buttons
    _render_navigation_buttons()
    
    # Warnings Panel
    _render_warnings_panel()
    
    st.markdown("</div>", unsafe_allow_html=True)


def _render_import_section() -> None:
    """Render the Import Scalar section."""
    st.markdown("<div class='pcgs-scalar-section'>", unsafe_allow_html=True)
    st.markdown("<div class='pcgs-scalar-section__title'>IMPORT SCALAR</div>", unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload Excel Template",
        type=["xlsx", "xls"],
        key="pcgs_scalar_upload",
        label_visibility="collapsed",
    )
    
    # Import button
    st.markdown("<div class='pcgs-pill-button pcgs-pill-button--primary'>", unsafe_allow_html=True)
    if st.button("IMPORT SCALAR", key="pcgs_scalar_import_btn"):
        if uploaded_file:
            success, message = scalar_service.import_scalar_from_file(uploaded_file)
            if success:
                st.success(message)
            else:
                st.error(message)
        else:
            st.warning("Please select an Excel file first.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown(
        "<div class='pcgs-scalar-help'>Import from Excel template (rows 6+, columns B–K).</div>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def _render_edit_tools() -> None:
    """Render the Edit Tools section."""
    st.markdown("<div class='pcgs-scalar-section'>", unsafe_allow_html=True)
    st.markdown("<div class='pcgs-scalar-section__title'>EDIT TOOLS</div>", unsafe_allow_html=True)
    
    current_mode = _get_edit_mode()
    
    cols = st.columns(4)
    for i, tool in enumerate(EDIT_TOOLS):
        with cols[i]:
            tool_key = tool.lower().replace(" ", "_")
            is_active = current_mode == tool_key
            btn_class = "pcgs-tool-button--active" if is_active else ""
            st.markdown(f"<div class='pcgs-tool-button {btn_class}'>", unsafe_allow_html=True)
            if st.button(tool, key=f"pcgs_scalar_tool_{tool_key}"):
                if is_active:
                    _set_edit_mode(None)
                else:
                    _set_edit_mode(tool_key)
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def _render_pke_control() -> None:
    """Render the Master PKE Control section."""
    st.markdown("<div class='pcgs-scalar-pke'>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='pcgs-pke-badge'>
        <span class='pcgs-pke-icon'>{PKE_ICON}</span>
        <span class='pcgs-pke-label'>PROMETHEUS: SCALAR BUILDER</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='pcgs-pill-button pcgs-pill-button--pke'>", unsafe_allow_html=True)
    if st.button("ENGAGE PKE", key="pcgs_scalar_pke"):
        st.session_state.setdefault("pcgs_ai_history", []).append(
            ("PKE", "Scalar Builder PKE functionality coming soon. I will help you generate and refine your course structure.")
        )
        st.info("PKE Scalar Builder engaged. See AI Console below.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def _render_navigation_buttons() -> None:
    """Render navigation buttons."""
    st.markdown("<div class='pcgs-scalar-nav'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='pcgs-pill-button pcgs-pill-button--neutral'>", unsafe_allow_html=True)
        if st.button("RETURN TO\nFRONT PAGE", key="pcgs_scalar_nav_back"):
            _navigate_to_tab("create")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='pcgs-pill-button pcgs-pill-button--neutral'>", unsafe_allow_html=True)
        if st.button("CONTINUE TO\nCONTENT MGR", key="pcgs_scalar_nav_forward"):
            _navigate_to_tab("content")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def _render_warnings_panel() -> None:
    """Render the Warnings panel."""
    warnings = scalar_service.get_warnings()
    
    st.markdown("<div class='pcgs-scalar-warnings'>", unsafe_allow_html=True)
    st.markdown("<div class='pcgs-scalar-section__title'>WARNINGS</div>", unsafe_allow_html=True)
    
    if warnings:
        for warning in warnings[-5:]:  # Show last 5 warnings
            st.markdown(f"<div class='pcgs-warning-item'>⚠️ {html.escape(warning)}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='pcgs-warning-empty'>No warnings.</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# Right Panel - Scalar Grid
# ============================================================================

def _render_grid_panel() -> None:
    """Render the right SCALAR GRID panel."""
    classes = "pcgs-panel pcgs-panel--scalar-grid"
    
    st.markdown(f"<div class='{classes}'>", unsafe_allow_html=True)
    st.markdown(
        "<div class='pcgs-panel__header'><div class='pcgs-panel__title'>COURSE SCALAR</div></div>",
        unsafe_allow_html=True,
    )
    
    # Create columns for the grid
    cols = st.columns(len(SCALAR_COLUMNS))
    
    for col_idx, col_config in enumerate(SCALAR_COLUMNS):
        with cols[col_idx]:
            _render_scalar_column(col_config)
    
    st.markdown("</div>", unsafe_allow_html=True)


def _render_scalar_column(config: Dict[str, Any]) -> None:
    """Render a single scalar column."""
    level = config["level"]
    label = config["label"]
    key = config["key"]
    
    # Get count
    count = scalar_service.get_level_count(level) if level else 0
    
    st.markdown(f"<div class='pcgs-scalar-column' data-level='{key}'>", unsafe_allow_html=True)
    
    # Header with label, PKE icon, and count
    st.markdown(f"""
    <div class='pcgs-scalar-column__header'>
        <span class='pcgs-scalar-column__label'>{label}</span>
        <span class='pcgs-scalar-column__pke'>{PKE_ICON}</span>
        <span class='pcgs-scalar-column__count'>({count})</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Content area
    st.markdown("<div class='pcgs-scalar-column__content'>", unsafe_allow_html=True)
    
    if level:
        entries = scalar_service.get_entries_for_display(level)
        
        if entries:
            for entry in entries:
                _render_entry_row(level, entry)
        else:
            st.markdown("<div class='pcgs-scalar-empty'>No items</div>", unsafe_allow_html=True)
        
        # Add entry row
        _render_add_entry_row(level, key)
    else:
        # Reserved column
        st.markdown("<div class='pcgs-scalar-reserved'>Reserved for future use</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def _render_entry_row(level: ScalarLevel, entry: Dict[str, Any]) -> None:
    """Render a single entry row."""
    serial = entry["serial"]
    text = entry["text"]
    is_editing = _is_editing(level, serial)
    edit_mode = _get_edit_mode()
    
    # Determine row state class
    row_class = "pcgs-scalar-row"
    if is_editing:
        row_class += " pcgs-scalar-row--edit"
    elif edit_mode == "delete":
        row_class += " pcgs-scalar-row--delete"
    
    st.markdown(f"<div class='{row_class}'>", unsafe_allow_html=True)
    
    if is_editing:
        # Edit mode - show inputs
        _render_edit_mode(level, serial, text)
    else:
        # Display mode
        truncated_text = text[:30] + "..." if len(text) > 30 else text
        
        col1, col2, col3 = st.columns([1, 5, 2])
        
        with col1:
            st.markdown(f"<span class='pcgs-scalar-row__serial'>{html.escape(serial)}</span>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"<span class='pcgs-scalar-row__text'>{html.escape(truncated_text)}</span>", unsafe_allow_html=True)
        
        with col3:
            # Action buttons based on edit mode
            if edit_mode == "delete":
                if st.button("🗑️", key=f"pcgs_del_{level.value}_{serial}"):
                    success, msg = scalar_service.delete_scalar_entry(level, serial)
                    if success:
                        st.rerun()
            elif edit_mode == "reorder":
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("↑", key=f"pcgs_up_{level.value}_{serial}"):
                        scalar_service.move_entry_up(level, serial)
                        st.rerun()
                with c2:
                    if st.button("↓", key=f"pcgs_down_{level.value}_{serial}"):
                        scalar_service.move_entry_down(level, serial)
                        st.rerun()
            else:
                if st.button("✏️", key=f"pcgs_edit_{level.value}_{serial}"):
                    _start_editing(level, serial)
                    st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)


def _render_edit_mode(level: ScalarLevel, serial: str, text: str) -> None:
    """Render edit mode for an entry."""
    new_serial = st.text_input(
        "Serial",
        value=serial,
        key=f"pcgs_edit_serial_{level.value}_{serial}",
        label_visibility="collapsed",
    )
    
    new_text = st.text_area(
        "Text",
        value=text,
        key=f"pcgs_edit_text_{level.value}_{serial}",
        height=60,
        label_visibility="collapsed",
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✔️", key=f"pcgs_confirm_{level.value}_{serial}"):
            success, msg = scalar_service.update_scalar_entry(
                level, serial, new_serial, new_text
            )
            _stop_editing()
            if success:
                st.rerun()
            else:
                st.error(msg)
    
    with col2:
        if st.button("✖️", key=f"pcgs_cancel_{level.value}_{serial}"):
            _stop_editing()
            st.rerun()


def _render_add_entry_row(level: ScalarLevel, key: str) -> None:
    """Render the add entry row at the bottom of a column."""
    st.markdown("<div class='pcgs-scalar-add-row'>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 5, 1])
    
    with col1:
        serial = st.text_input(
            "Serial",
            key=f"pcgs_add_serial_{key}",
            placeholder=scalar_service.get_next_serial(level),
            label_visibility="collapsed",
        )
    
    with col2:
        text = st.text_input(
            "Text",
            key=f"pcgs_add_text_{key}",
            placeholder="Enter text...",
            label_visibility="collapsed",
        )
    
    with col3:
        if st.button("+", key=f"pcgs_add_btn_{key}"):
            if text.strip():
                success, msg = scalar_service.add_scalar_entry(level, serial, text)
                if success:
                    # Clear inputs
                    st.session_state[f"pcgs_add_serial_{key}"] = ""
                    st.session_state[f"pcgs_add_text_{key}"] = ""
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.warning("Please enter text content.")
    
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# AI Console
# ============================================================================

def _render_ai_band() -> None:
    """Render the AI console band."""
    st.markdown("<div class='pcgs-ai-band'>", unsafe_allow_html=True)
    st.markdown("<div class='pcgs-ai-band__header'>PROMETHEUS AI</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='pcgs-ai-band__feed'>", unsafe_allow_html=True)
    history = st.session_state.get("pcgs_ai_history", [
        ("PKE", "PROMETHEUS Knowledge Engine calibrated. Scalar Builder ready.")
    ])
    
    for speaker, text in history[-10:]:
        prefix = "[PKE]" if speaker == "PKE" else ">"
        st.markdown(
            f"<div class='pcgs-ai-band__line'><span class='pcgs-ai-band__speaker'>{prefix}</span>{html.escape(text)}</div>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='pcgs-ai-band__prompt'>PROMPT<span class='pcgs-ai-band__caret'></span></div>", unsafe_allow_html=True)
    st.text_input(
        "PKE Input",
        key="pcgs_scalar_ai_input",
        label_visibility="collapsed",
        placeholder="Type your request and press Enter…",
    )
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# Footer
# ============================================================================

def _render_footer() -> None:
    """Render the bottom status strip."""
    counts = scalar_service.get_all_counts()
    total_entries = sum(counts.values())
    progress = min(100, int((total_entries / 20) * 100)) if total_entries else 0
    
    st.markdown("<div class='pcgs-footer'>", unsafe_allow_html=True)
    st.markdown(f"<div><strong>Owner:</strong> {CURRENT_USER.upper()}</div>", unsafe_allow_html=True)
    st.markdown(f"<div><strong>Start Date:</strong> {START_DATE}</div>", unsafe_allow_html=True)
    st.markdown(f"<div><strong>Status:</strong> {PROGRAM_STATUS}</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div><strong>Progress:</strong> {progress}%"
        f"<div class='pcgs-progress'><div class='pcgs-progress__value' style='width: {progress}%;'></div></div></div>",
        unsafe_allow_html=True,
    )
    st.markdown(f"<div><strong>Approved for Use Y/N:</strong> {APPROVED_FOR_USE}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# Navigation
# ============================================================================

def _navigate_to_tab(tab_id: str) -> None:
    """Navigate to a different tab."""
    st.session_state[NAV_STATE_KEY] = tab_id
    st.info(f"Navigation to {tab_id} - Tab switching will be implemented in the main app shell.")


# ============================================================================
# Styles
# ============================================================================

def _inject_scalar_styles() -> None:
    """Inject Scalar Manager specific CSS styles."""
    css = """
    <style>
    /* Scalar Manager specific layout */
    .pcgs-scalar-root {
        grid-template-areas:
            "status status"
            "left right"
            "left right"
            "ai ai"
            "footer footer" !important;
        grid-template-columns: minmax(300px, 0.35fr) minmax(600px, 1fr) !important;
    }
    
    .pcgs-region-scalar-left {
        grid-area: left;
    }
    
    .pcgs-region-scalar-right {
        grid-area: right;
    }
    
    .pcgs-header-status__page-title {
        color: #2CF0FF;
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: 0.2em;
        margin-top: 0.3rem;
    }
    
    /* Control Panel Sections */
    .pcgs-scalar-section {
        background: rgba(6, 12, 24, 0.6);
        border-radius: 14px;
        border: 1px solid rgba(44, 240, 255, 0.2);
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .pcgs-scalar-section__title {
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.15em;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 0.75rem;
        text-transform: uppercase;
    }
    
    .pcgs-scalar-help {
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.5);
        margin-top: 0.5rem;
    }
    
    /* Edit Tools */
    .pcgs-tool-button {
        padding: 2px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        background: rgba(0, 0, 0, 0.3);
    }
    
    .pcgs-tool-button button {
        font-size: 0.65rem !important;
        padding: 0.4rem 0.2rem !important;
        letter-spacing: 0.05em;
    }
    
    .pcgs-tool-button--active {
        border-color: #2CF0FF;
        background: rgba(44, 240, 255, 0.15);
        box-shadow: 0 0 10px rgba(44, 240, 255, 0.3);
    }
    
    /* PKE Control */
    .pcgs-scalar-pke {
        background: linear-gradient(135deg, rgba(255, 179, 71, 0.15), rgba(255, 179, 71, 0.05));
        border-radius: 14px;
        border: 1px solid rgba(255, 179, 71, 0.4);
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .pcgs-pke-badge {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 0.75rem;
    }
    
    .pcgs-pke-icon {
        font-size: 1.5rem;
    }
    
    .pcgs-pke-label {
        color: #FFB347;
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 0.1em;
    }
    
    .pcgs-pill-button--pke {
        border-color: rgba(255, 179, 71, 0.6);
        background: rgba(255, 179, 71, 0.1);
    }
    
    .pcgs-pill-button--pke button {
        color: #FFB347 !important;
    }
    
    /* Navigation Buttons */
    .pcgs-scalar-nav {
        margin-bottom: 1rem;
    }
    
    .pcgs-scalar-nav .pcgs-pill-button button {
        font-size: 0.7rem !important;
        padding: 0.6rem 0.3rem !important;
        white-space: pre-line;
        line-height: 1.3;
    }
    
    /* Warnings Panel */
    .pcgs-scalar-warnings {
        background: rgba(6, 12, 24, 0.6);
        border-radius: 14px;
        border: 1px solid rgba(247, 227, 116, 0.3);
        padding: 1rem;
    }
    
    .pcgs-warning-item {
        font-size: 0.75rem;
        color: #F7E374;
        margin-bottom: 0.4rem;
        padding: 0.3rem 0.5rem;
        background: rgba(247, 227, 116, 0.1);
        border-radius: 6px;
    }
    
    .pcgs-warning-empty {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.4);
        font-style: italic;
    }
    
    /* Scalar Grid */
    .pcgs-panel--scalar-grid {
        display: flex;
        flex-direction: column;
        min-height: 500px;
    }
    
    .pcgs-scalar-column {
        background: rgba(6, 12, 24, 0.5);
        border-radius: 12px;
        border: 1px solid rgba(44, 240, 255, 0.25);
        padding: 0.75rem;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .pcgs-scalar-column__header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(44, 240, 255, 0.2);
        margin-bottom: 0.5rem;
    }
    
    .pcgs-scalar-column__label {
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        color: rgba(255, 255, 255, 0.9);
        flex: 1;
    }
    
    .pcgs-scalar-column__pke {
        font-size: 0.9rem;
        cursor: pointer;
    }
    
    .pcgs-scalar-column__count {
        font-size: 0.7rem;
        color: rgba(255, 255, 255, 0.5);
    }
    
    .pcgs-scalar-column__content {
        flex: 1;
        overflow-y: auto;
        max-height: 350px;
    }
    
    /* Scalar Rows */
    .pcgs-scalar-row {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 6px;
        border: 1px solid rgba(44, 240, 255, 0.15);
        padding: 0.4rem 0.5rem;
        margin-bottom: 0.4rem;
        transition: all 0.2s ease;
    }
    
    .pcgs-scalar-row:hover {
        border-color: rgba(98, 255, 183, 0.5);
        background: rgba(98, 255, 183, 0.05);
    }
    
    .pcgs-scalar-row:hover .pcgs-scalar-row__serial,
    .pcgs-scalar-row:hover .pcgs-scalar-row__text {
        color: #62FFB7 !important;
    }
    
    .pcgs-scalar-row--edit {
        border-color: rgba(255, 179, 71, 0.6);
        background: rgba(255, 179, 71, 0.1);
    }
    
    .pcgs-scalar-row--delete {
        border-color: rgba(255, 77, 109, 0.5);
    }
    
    .pcgs-scalar-row--delete:hover {
        border-color: rgba(255, 77, 109, 0.8);
        background: rgba(255, 77, 109, 0.1);
    }
    
    .pcgs-scalar-row__serial {
        font-size: 0.7rem;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.6);
        min-width: 30px;
    }
    
    .pcgs-scalar-row__text {
        font-size: 0.7rem;
        color: rgba(255, 255, 255, 0.85);
    }
    
    /* Add Entry Row */
    .pcgs-scalar-add-row {
        margin-top: auto;
        padding-top: 0.5rem;
        border-top: 1px dashed rgba(44, 240, 255, 0.2);
    }
    
    .pcgs-scalar-add-row input {
        font-size: 0.7rem !important;
        padding: 0.3rem 0.5rem !important;
    }
    
    .pcgs-scalar-empty {
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.3);
        text-align: center;
        padding: 2rem 0.5rem;
        font-style: italic;
    }
    
    .pcgs-scalar-reserved {
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.3);
        text-align: center;
        padding: 3rem 0.5rem;
        font-style: italic;
    }
    
    /* Disabled button style */
    .pcgs-pill-button--disabled {
        opacity: 0.4;
    }
    
    .pcgs-pill-button--disabled button {
        cursor: not-allowed !important;
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    /* AI Console adjustments */
    .pcgs-scalar-root .pcgs-ai-band__header {
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.15em;
        color: rgba(31, 19, 2, 0.7);
        margin-bottom: 0.5rem;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
