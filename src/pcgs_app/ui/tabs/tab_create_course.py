"""
Create Course / CLO Tab

Implements the Prometheus v2 console layout for Tab 1 – Create Course.
"""

import copy
import html
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

import streamlit as st

from pcgs_app.logic.lexicon import Lex
from pcgs_app.ui.theme.shared_chrome import (
    render_footer,
    render_ai_console,
    navigate_to_tab,
    inject_shared_chrome_styles,
    CURRENT_USER,
    START_DATE,
    PROGRAM_STATUS,
    APPROVED_FOR_USE,
    PKE_ICON,
    HISTORY_LIMIT,
)
from pcgs_app.ui.theme.streamlit_theme import apply_base_theme
from pcgs_app.ui.theme.tokens import ICONS, get_default_tokens
from pcgs_app.ui.widgets.status_lights import render_status_dot

NEW_COURSE_LABEL = "-- NEW COURSE --"

COURSE_LEVEL_OPTIONS = ["", "Foundation", "Intermediate", "Advanced", "Executive"]
COURSE_THEMATIC_OPTIONS = [
    "",
    "Cyber Operations",
    "Leadership",
    "Prometheus Systems",
    "Strategic Planning",
    "Readiness",
]

EXPORT_BUTTONS = [
    ("PRESENTATION", "presentation"),
    ("HANDBOOK", "handbook"),
    ("ASSESSMENTS", "assessments"),
    ("SUPPORTING MATERIALS", "supporting_materials"),
]

MANAGER_TILES = [
    ("SCALAR MANAGER", "scalar", Lex.SCALEMGR),
    ("CONTENT MANAGER", "content", Lex.CONTMGR),
    ("LESSON MANAGER", "lesson", Lex.LSNMGR),
]

COURSE_FLOW_SEQUENCE = [Lex.C_INFO, Lex.C_DESC, Lex.CLO, Lex.SCALEMGR, Lex.CONTMGR, Lex.LSNMGR]

MIN_CLOS = 3

DEFAULT_COURSE_INFO: Dict[Lex, str] = {
    Lex.C_NAME: "",
    Lex.C_LEVEL: "",
    Lex.C_THEME: "",
    Lex.C_DURATION: "",
    Lex.C_CODE: "",
    Lex.C_DEV: CURRENT_USER,
}

DEFAULT_CLOS: List[str] = ["", "", ""]

PLACEHOLDER_DESCRIPTION = (
    "This is placeholder text. PKE functionality coming soon. "
    "Your generated course description will appear here."
)

CLO_PLACEHOLDERS = [
    "CLO 1 – Placeholder objective drafted by PKE preview.",
    "CLO 2 – Placeholder objective drafted by PKE preview.",
    "CLO 3 – Placeholder objective drafted by PKE preview.",
    "CLO 4 – Placeholder objective drafted by PKE preview.",
]

CLO_ALT_PLACEHOLDERS = [
    "CLO 1 – Alternate placeholder objective supplied by PKE.",
    "CLO 2 – Alternate placeholder objective supplied by PKE.",
    "CLO 3 – Alternate placeholder objective supplied by PKE.",
    "CLO 4 – Alternate placeholder objective supplied by PKE.",
]

AI_PROMPTS: Dict[str, str] = {
    "description": "Would you like me to draft a course description based on the current Course Information?",
    "clos": "Would you like me to suggest Course Learning Objectives based on your course description?",
    "scalar": "Would you like me to propose scalar entries for this course?",
    "content": "Would you like me to propose a content structure for this course?",
    "lesson": "Would you like me to propose a lesson sequence for this course?",
}

MANAGER_MESSAGES = {
    "scalar": "PKE functionality for Scalar Manager is coming soon. This node will eventually help build your scalar entries.",
    "content": "PKE functionality for Content Manager is coming soon. This node will eventually help build your content structure.",
    "lesson": "PKE functionality for Lesson Manager is coming soon. This node will eventually help build your lesson sequence.",
}

STEP_FLAG_KEYS: Dict[Lex, str] = {
    Lex.C_INFO: "pcgs_step_courseinfo_complete",
    Lex.C_DESC: "pcgs_step_description_complete",
    Lex.CLO: "pcgs_step_clo_complete",
    Lex.SCALEMGR: "pcgs_step_scalar_complete",
    Lex.CONTMGR: "pcgs_step_content_complete",
    Lex.LSNMGR: "pcgs_step_lesson_complete",
}

CONNECTOR_EDGES = [
    (Lex.C_INFO, Lex.C_DESC),
    (Lex.C_DESC, Lex.CLO),
    (Lex.CLO, Lex.SCALEMGR),
    (Lex.SCALEMGR, Lex.CONTMGR),
    (Lex.CONTMGR, Lex.LSNMGR),
]

PROGRESS_STEPS = [Lex.C_DESC, Lex.CLO, Lex.SCALEMGR, Lex.CONTMGR, Lex.LSNMGR]

PKE_TARGET_TO_STAGE: Dict[str, Optional[Lex]] = {
    "description": Lex.C_DESC,
    "clos": Lex.CLO,
    "scalar": Lex.SCALEMGR,
    "content": Lex.CONTMGR,
    "lesson": Lex.LSNMGR,
}

COURSE_LIBRARY: Dict[str, Dict[str, Any]] = {
    "Cyber Defense Analyst Bootcamp": {
        "title": "Cyber Defense Analyst Bootcamp",
        "level": "Intermediate",
        "thematic": "Cyber Operations",
        "duration": "5 days",
        "code": "CDA-205",
        "developer": CURRENT_USER,
        "description": "Participants master Prometheus detection tooling and run live-fire blue-team exercises.",
        "clos": [
            "CLO 1 – Detect, document, and triage priority incidents within Prometheus infrastructure.",
            "CLO 2 – Apply layered response playbooks across SOC, hunt, and intel functions.",
            "CLO 3 – Brief senior leadership on threat posture and readiness metrics.",
        ],
    },
    "Prometheus Leadership Foundations": {
        "title": "Prometheus Leadership Foundations",
        "level": "Executive",
        "thematic": "Leadership",
        "duration": "3 days",
        "code": "PLF-101",
        "developer": CURRENT_USER,
        "description": "Exec-level orientation to the Prometheus operating model and cultural tenets.",
        "clos": [
            "CLO 1 – Explain the Prometheus decision cycles and escalation ladders.",
            "CLO 2 – Coach functional leads on AI-aligned empowerment models.",
            "CLO 3 – Align strategic initiatives with PCGS governance checkpoints.",
        ],
    },
}

COURSE_OPTIONS = [NEW_COURSE_LABEL, *COURSE_LIBRARY.keys()]

COURSE_INFO_WIDGET_KEYS: Dict[Lex, str] = {
    Lex.C_NAME: "pcgs_course_title",
    Lex.C_LEVEL: "pcgs_course_level",
    Lex.C_THEME: "pcgs_course_thematic",
    Lex.C_DURATION: "pcgs_course_duration",
    Lex.C_CODE: "pcgs_course_code",
    Lex.C_DEV: "pcgs_course_developer",
}

DESCRIPTION_INPUT_KEY = "pcgs_course_description_text"


def render_tab_create_course(course: Optional[Dict[str, Any]] = None) -> None:
    """
    Render the sci-fi styled Create Course hub with Prometheus v2 layout.
    """

    apply_base_theme(get_default_tokens())
    inject_shared_chrome_styles()
    _init_state(course)
    _tick_ai_flash()
    _update_completion_flags()

    st.markdown("<div class='pcgs-root'>", unsafe_allow_html=True)
    _render_region("pcgs-region-status", _render_header)
    _render_region("pcgs-region-select", _render_select_course)
    _render_region("pcgs-region-course-info", _render_course_info_panel)
    _render_region("pcgs-region-generate", _render_exports_panel)
    _render_region("pcgs-region-learning", _render_clos_panel)
    _render_region("pcgs-region-course-desc", _render_description_panel)
    _render_region("pcgs-region-connectors", _render_connectors)
    _render_region("pcgs-region-managers", _render_managers_row)
    _render_region("pcgs-region-ai", _render_ai_band)
    _render_region("pcgs-region-footer", _render_footer_section)
    st.markdown("</div>", unsafe_allow_html=True)


def _render_region(region_class: str, renderer: Callable[[], None]) -> None:
    with st.container():
        st.markdown(f"<div class='{region_class}'>", unsafe_allow_html=True)
        renderer()
        st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# State helpers
# ---------------------------------------------------------------------------


def _init_state(initial_course: Optional[Dict[str, Any]]) -> None:
    state = st.session_state

    if "pcgs_course_info" not in state:
        state["pcgs_course_info"] = copy.deepcopy(DEFAULT_COURSE_INFO)
    if "pcgs_course_description" not in state:
        state["pcgs_course_description"] = ""
    if "pcgs_clos" not in state:
        state["pcgs_clos"] = copy.deepcopy(DEFAULT_CLOS)
    if "pcgs_saved_snapshot" not in state:
        state["pcgs_saved_snapshot"] = _build_snapshot()
    if "pcgs_ai_history" not in state:
        state["pcgs_ai_history"] = [
            ("PKE", "PROMETHEUS Knowledge Engine calibrated. Awaiting trigger.")
        ]
    state.setdefault("pcgs_ai_mode", "idle")
    state.setdefault("pcgs_ai_followup", None)
    state.setdefault("pcgs_ai_target_panel", None)
    state.setdefault("pcgs_ai_flash_panel", None)
    state.setdefault("pcgs_ai_flash_ticks", 0)
    state.setdefault("pcgs_ai_input", "")
    state.setdefault("pcgs_ai_input_triggered", False)
    state.setdefault("pcgs_has_saved_once", False)
    state.setdefault("pcgs_selected_course_option", NEW_COURSE_LABEL)
    state.setdefault("pcgs_active_course_option", NEW_COURSE_LABEL)

    for key in STEP_FLAG_KEYS.values():
        state.setdefault(key, False)

    _ensure_min_clos()

    if initial_course:
        _apply_external_course(initial_course, mark_saved=True, show_message=False)

    _sync_form_inputs()


def _ensure_min_clos(min_count: int = MIN_CLOS) -> None:
    clos = st.session_state["pcgs_clos"]
    if len(clos) < min_count:
        clos.extend([""] * (min_count - len(clos)))


def _sync_form_inputs() -> None:
    info = st.session_state["pcgs_course_info"]
    for field, key in COURSE_INFO_WIDGET_KEYS.items():
        value = info.get(field, "")
        st.session_state[key] = value

    st.session_state[DESCRIPTION_INPUT_KEY] = st.session_state["pcgs_course_description"]

    for idx, value in enumerate(st.session_state["pcgs_clos"]):
        st.session_state[f"pcgs_clo_{idx}"] = value


def _build_snapshot() -> Dict[str, Any]:
    return {
        "course_info": copy.deepcopy(st.session_state.get("pcgs_course_info", {})),
        "description": st.session_state.get("pcgs_course_description", ""),
        "clos": copy.deepcopy(st.session_state.get("pcgs_clos", [])),
    }


def _apply_external_course(
    payload: Dict[str, Any],
    *,
    mark_saved: bool,
    show_message: bool,
) -> None:
    info = copy.deepcopy(DEFAULT_COURSE_INFO)
    info[Lex.C_NAME] = payload.get("title") or payload.get("name") or info[Lex.C_NAME]
    info[Lex.C_LEVEL] = payload.get("level", info[Lex.C_LEVEL])
    info[Lex.C_THEME] = payload.get("thematic") or payload.get("theme") or info[Lex.C_THEME]
    duration_value = payload.get("duration")
    if not duration_value:
        duration_days = payload.get("duration_days")
        if duration_days is not None:
            duration_value = f"{duration_days}"
    info[Lex.C_DURATION] = duration_value or info[Lex.C_DURATION]
    info[Lex.C_CODE] = payload.get("code", info[Lex.C_CODE])
    info[Lex.C_DEV] = payload.get("developer", info[Lex.C_DEV])

    st.session_state["pcgs_course_info"] = info
    st.session_state["pcgs_course_description"] = payload.get("description", "")
    clos = payload.get("clos") or payload.get("learning_objectives") or []
    st.session_state["pcgs_clos"] = list(clos) if isinstance(clos, list) else copy.deepcopy(DEFAULT_CLOS)

    _ensure_min_clos()
    _sync_form_inputs()

    if mark_saved:
        st.session_state["pcgs_saved_snapshot"] = _build_snapshot()
        st.session_state["pcgs_has_saved_once"] = True
        _update_completion_flags()
    else:
        _update_completion_flags()

    if show_message:
        st.success("Course loaded.")


def _reset_course_editor(
    *,
    show_message: bool,
    reset_selection: bool,
) -> None:
    st.session_state["pcgs_course_info"] = copy.deepcopy(DEFAULT_COURSE_INFO)
    st.session_state["pcgs_course_description"] = ""
    st.session_state["pcgs_clos"] = copy.deepcopy(DEFAULT_CLOS)
    st.session_state["pcgs_saved_snapshot"] = _build_snapshot()
    st.session_state["pcgs_has_saved_once"] = False
    st.session_state["pcgs_ai_target_panel"] = None
    st.session_state["pcgs_ai_flash_panel"] = None
    st.session_state["pcgs_ai_flash_ticks"] = 0
    st.session_state["pcgs_ai_followup"] = None
    for key in STEP_FLAG_KEYS.values():
        st.session_state[key] = False
    _ensure_min_clos()
    _sync_form_inputs()
    _update_completion_flags()

    if reset_selection:
        st.session_state["pcgs_selected_course_option"] = NEW_COURSE_LABEL
        st.session_state["pcgs_active_course_option"] = NEW_COURSE_LABEL

    if show_message:
        st.info("Editor reset. Ready for a new course.")


# ---------------------------------------------------------------------------
# Header + controls
# ---------------------------------------------------------------------------


def _render_header() -> None:
    st.markdown("<div class='pcgs-status-band'>", unsafe_allow_html=True)
    st.markdown("<div class='pcgs-status-band__left'>", unsafe_allow_html=True)
    _render_header_status()
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='pcgs-status-band__right'>", unsafe_allow_html=True)
    _render_top_buttons()
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def _render_header_status() -> None:
    info = st.session_state["pcgs_course_info"]
    now_str = datetime.now().strftime("%d %b %Y %H:%M")
    title = info.get(Lex.C_NAME, "") or "UNSPECIFIED"
    duration = info.get(Lex.C_DURATION, "") or "N/A"
    level = info.get(Lex.C_LEVEL, "") or "UNSPECIFIED"
    thematic = info.get(Lex.C_THEME, "") or "UNSPECIFIED"

    status_html = f"""
    <div class="pcgs-header-status">
        <div class="pcgs-header-status__title">PROMETHEUS COURSE GENERATION SYSTEM 2.0</div>
        <div class="pcgs-header-status__timestamp">{now_str}</div>
        <div class="pcgs-header-status__metrics">
            <span>Course Loaded · {html.escape(title)}</span>
            <span>Duration · {html.escape(duration)}</span>
            <span>Level · {html.escape(level)}</span>
            <span>Thematic · {html.escape(thematic)}</span>
        </div>
    </div>
    """
    st.markdown(status_html, unsafe_allow_html=True)


def _render_top_buttons() -> None:
    """Render horizontal action buttons in the header."""
    specs = [
        ("LOAD", "neutral", _handle_load_button),
        ("SAVE", "primary", _handle_save_button),
        ("DELETE", "danger", _handle_delete_button),
        ("RESET", "neutral", _handle_clear_button),
    ]
    # Use horizontal layout for dashboard
    st.markdown("<div class='pcgs-top-buttons--horizontal'>", unsafe_allow_html=True)
    for label, tone, handler in specs:
        st.markdown(
            f"<div class='pcgs-pill-button pcgs-pill-button--{tone}'>",
            unsafe_allow_html=True,
        )
        if st.button(label, key=f"pcgs_ctrl_{label.lower().replace('/', '_').replace(' ', '_')}"):
            handler()
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def _handle_load_button() -> None:
    selected = st.session_state.get("pcgs_selected_course_option", NEW_COURSE_LABEL)
    if selected == NEW_COURSE_LABEL:
        example = next(iter(COURSE_LIBRARY.values()))
        _apply_external_course(example, mark_saved=False, show_message=False)
        st.info("Starter template loaded. Press SAVE to lock it in.")
    else:
        payload = COURSE_LIBRARY.get(selected)
        if payload:
            _apply_external_course(payload, mark_saved=True, show_message=True)
            st.session_state["pcgs_active_course_option"] = selected


def _handle_save_button() -> None:
    st.session_state["pcgs_saved_snapshot"] = _build_snapshot()
    st.session_state["pcgs_has_saved_once"] = True
    _update_completion_flags()
    st.success("Course saved (placeholder).")


def _handle_delete_button() -> None:
    _reset_course_editor(show_message=False, reset_selection=True)
    st.warning("Course deleted from the working session (placeholder).")


def _handle_clear_button() -> None:
    _reset_course_editor(show_message=True, reset_selection=False)


# ---------------------------------------------------------------------------
# Course selection + panels
# ---------------------------------------------------------------------------


def _render_select_course() -> None:
    st.markdown("<div class='pcgs-select-course'>", unsafe_allow_html=True)
    selected = st.selectbox(
        "SELECT COURSE",
        COURSE_OPTIONS,
        key="pcgs_selected_course_option",
        help="Load a stored course or start a new build.",
    )
    st.markdown("</div>", unsafe_allow_html=True)
    _handle_course_selection(selected)


def _handle_course_selection(selected: str) -> None:
    active = st.session_state.get("pcgs_active_course_option", NEW_COURSE_LABEL)
    if selected == active:
        return
    st.session_state["pcgs_active_course_option"] = selected
    if selected == NEW_COURSE_LABEL:
        _reset_course_editor(show_message=False, reset_selection=False)
    else:
        payload = COURSE_LIBRARY.get(selected)
        if payload:
            _apply_external_course(payload, mark_saved=True, show_message=False)


def _render_course_info_panel() -> None:
    stage = Lex.C_INFO
    classes = _panel_classes("pcgs-panel--course-info", stage=stage)
    status = render_status_dot(_panel_status(stage))

    st.markdown(f"<div class='{classes}'>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='pcgs-panel__header'><div class='pcgs-panel__title'>{status} COURSE INFORMATION</div></div>",
        unsafe_allow_html=True,
    )

    info = st.session_state["pcgs_course_info"]
    cols = st.columns(2)
    with cols[0]:
        title = st.text_input(
            "Title",
            key=COURSE_INFO_WIDGET_KEYS[Lex.C_NAME],
            value=st.session_state[COURSE_INFO_WIDGET_KEYS[Lex.C_NAME]],
        )
        info[Lex.C_NAME] = title
        duration = st.text_input(
            "Duration",
            key=COURSE_INFO_WIDGET_KEYS[Lex.C_DURATION],
            value=st.session_state[COURSE_INFO_WIDGET_KEYS[Lex.C_DURATION]],
        )
        info[Lex.C_DURATION] = duration
        code = st.text_input(
            "Code",
            key=COURSE_INFO_WIDGET_KEYS[Lex.C_CODE],
            value=st.session_state[COURSE_INFO_WIDGET_KEYS[Lex.C_CODE]],
        )
        info[Lex.C_CODE] = code
    with cols[1]:
        level = st.selectbox(
            "Level",
            _ensure_option(COURSE_LEVEL_OPTIONS, st.session_state[COURSE_INFO_WIDGET_KEYS[Lex.C_LEVEL]]),
            key=COURSE_INFO_WIDGET_KEYS[Lex.C_LEVEL],
        )
        info[Lex.C_LEVEL] = level
        thematic = st.selectbox(
            "Thematic",
            _ensure_option(COURSE_THEMATIC_OPTIONS, st.session_state[COURSE_INFO_WIDGET_KEYS[Lex.C_THEME]]),
            key=COURSE_INFO_WIDGET_KEYS[Lex.C_THEME],
        )
        info[Lex.C_THEME] = thematic
        developer = st.text_input(
            "Developer",
            key=COURSE_INFO_WIDGET_KEYS[Lex.C_DEV],
            value=st.session_state[COURSE_INFO_WIDGET_KEYS[Lex.C_DEV]],
        )
        info[Lex.C_DEV] = developer

    st.session_state["pcgs_course_info"] = info
    st.markdown("</div>", unsafe_allow_html=True)


def _render_description_panel() -> None:
    stage = Lex.C_DESC
    classes = _panel_classes("pcgs-panel--description", stage=stage)
    status = render_status_dot(_panel_status(stage))

    st.markdown(f"<div class='{classes}'>", unsafe_allow_html=True)
    header_cols = st.columns([4, 1])
    with header_cols[0]:
        st.markdown(
            f"<div class='pcgs-panel__title'>{status} COURSE DESCRIPTION</div>",
            unsafe_allow_html=True,
        )
    with header_cols[1]:
        _render_flame_button("description")
    description = st.text_area(
        "Course Description",
        key=DESCRIPTION_INPUT_KEY,
        value=st.session_state[DESCRIPTION_INPUT_KEY],
        height=220,
    )
    st.session_state["pcgs_course_description"] = description
    st.markdown("</div>", unsafe_allow_html=True)


def _render_clos_panel() -> None:
    stage = Lex.CLO
    classes = _panel_classes("pcgs-panel--clos", stage=stage)
    status = render_status_dot(_panel_status(stage))

    st.markdown(f"<div class='{classes}'>", unsafe_allow_html=True)
    header_cols = st.columns([4, 1, 1])
    with header_cols[0]:
        st.markdown(
            f"<div class='pcgs-panel__title'>{status} LEARNING OBJECTIVES</div>",
            unsafe_allow_html=True,
        )
    with header_cols[1]:
        st.markdown("<div class='pcgs-mini-button'>", unsafe_allow_html=True)
        if st.button("+", key="pcgs_add_clo", help="Add Learning Objective"):
            _add_clo_row()
        st.markdown("</div>", unsafe_allow_html=True)
    with header_cols[2]:
        _render_flame_button("clos")

    st.markdown("<div class='pcgs-clos-list'>", unsafe_allow_html=True)
    for idx, value in enumerate(st.session_state["pcgs_clos"]):
        text = st.text_area(
            f"CLO {idx + 1}",
            key=f"pcgs_clo_{idx}",
            value=st.session_state.get(f"pcgs_clo_{idx}", value),
            height=85,
        )
        st.session_state["pcgs_clos"][idx] = text
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def _render_exports_panel() -> None:
    classes = _panel_classes("pcgs-panel--export")
    st.markdown(f"<div class='{classes}'>", unsafe_allow_html=True)
    st.markdown(
        "<div class='pcgs-panel__header'><div class='pcgs-panel__title'>GENERATE</div></div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='pcgs-generate-buttons'>", unsafe_allow_html=True)
    for label, key_suffix in EXPORT_BUTTONS:
        st.markdown("<div class='pcgs-pill-button pcgs-pill-button--neutral'>", unsafe_allow_html=True)
        if st.button(label, key=f"pcgs_export_{key_suffix}"):
            st.info("Export not yet implemented.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Flow connectors + manager tiles
# ---------------------------------------------------------------------------


def _render_connectors() -> None:
    st.markdown("<div class='pcgs-connector-row'>", unsafe_allow_html=True)
    for left, right in CONNECTOR_EDGES:
        state = _connector_state(left, right)
        classes = f"pcgs-connector pcgs-connector--{state}"
        st.markdown(f"<div class='{classes}'></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def _render_managers_row() -> None:
    st.markdown("<div class='pcgs-managers-row'>", unsafe_allow_html=True)
    st.markdown("<div class='pcgs-node-row'>", unsafe_allow_html=True)
    for label, mode, stage in MANAGER_TILES:
        classes = _tile_classes(stage)
        status = render_status_dot(_panel_status(stage))
        st.markdown(f"<div class='{classes}'>", unsafe_allow_html=True)
        meta_cols = st.columns([3, 1])
        with meta_cols[0]:
            st.markdown(
                f"<div class='pcgs-panel__title'>{status} {label}</div>",
                unsafe_allow_html=True,
            )
        with meta_cols[1]:
            _render_flame_button(mode)
        if st.button(
            f"OPEN {label}",
            key=f"pcgs_manager_{mode}",
        ):
            _navigate_to_manager(mode, label)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def _navigate_to_manager(mode: str, label: str) -> None:
    """
    Navigate to a manager tab.
    Sets session state that the main app shell can read to switch tabs.
    
    Args:
        mode: Tab mode identifier ("scalar", "content", "lesson")
        label: Display label for the tab
    """
    # Map mode to tab id
    tab_map = {
        "scalar": "scalar",
        "content": "content", 
        "lesson": "lessons",
    }
    tab_id = tab_map.get(mode, mode)
    navigate_to_tab(tab_id)
    st.info(f"Navigating to {label}. Select the tab from the sidebar to continue.")


# ---------------------------------------------------------------------------
# AI band + footer
# ---------------------------------------------------------------------------


def _render_ai_band() -> None:
    active = st.session_state.get("pcgs_ai_mode") != "idle"
    band_class = "pcgs-ai-band pcgs-ai-band--active" if active else "pcgs-ai-band"

    st.markdown(f"<div class='{band_class}'>", unsafe_allow_html=True)
    st.markdown("<div class='pcgs-ai-band__feed'>", unsafe_allow_html=True)
    for speaker, text in st.session_state["pcgs_ai_history"][-HISTORY_LIMIT:]:
        prefix = "[PKE]" if speaker == "PKE" else "&gt;"
        st.markdown(
            f"<div class='pcgs-ai-band__line'><span class='pcgs-ai-band__speaker'>{prefix}</span>{_sanitize(text)}</div>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='pcgs-ai-band__prompt'>PROMPT<span class='pcgs-ai-band__caret'></span></div>", unsafe_allow_html=True)
    st.text_input(
        "PKE Input",
        key="pcgs_ai_input",
        label_visibility="collapsed",
        placeholder="Type your reply and press Enter…",
        on_change=_flag_ai_submission,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.pop("pcgs_ai_input_triggered", False):
        _handle_ai_submission()


def _render_footer_section() -> None:
    """Render the footer using shared chrome component."""
    total = len(PROGRESS_STEPS)
    completed = sum(1 for stage in PROGRESS_STEPS if _stage_complete(stage))
    progress = round((completed / total) * 100) if total else 0
    render_footer(progress_percent=progress)


# ---------------------------------------------------------------------------
# AI helpers
# ---------------------------------------------------------------------------


def _flag_ai_submission() -> None:
    st.session_state["pcgs_ai_input_triggered"] = True


def _handle_ai_submission() -> None:
    raw_input = st.session_state.get("pcgs_ai_input", "")
    reply = raw_input.strip()
    if not reply:
        return

    _append_user_line(reply)
    st.session_state["pcgs_ai_input"] = ""
    active_stage = st.session_state.get("pcgs_ai_target_panel")
    _process_ai_reply(reply)
    if st.session_state.get("pcgs_ai_mode") == "idle" and active_stage is not None:
        _flash_panel(active_stage)
        _set_ai_target(None)


def _process_ai_reply(reply: str) -> None:
    mode = st.session_state.get("pcgs_ai_mode", "idle")
    lowered = reply.lower()

    if mode == "description":
        _handle_description_reply(lowered)
        st.session_state["pcgs_ai_mode"] = "idle"
        return

    if mode == "clos":
        _handle_clos_reply(lowered)
        return

    if mode in {"scalar", "content", "lesson"}:
        _handle_manager_reply(mode)
        st.session_state["pcgs_ai_mode"] = "idle"
        return

    _append_ai_line("Input received. Engage a flame icon to target a panel.")


def _handle_description_reply(reply: str) -> None:
    if "yes" in reply:
        st.session_state["pcgs_course_description"] = PLACEHOLDER_DESCRIPTION
        st.session_state["pcgs_ai_target_panel"] = Lex.C_DESC
        _sync_form_inputs()
        _append_ai_line("Draft description generated and placed into the Course Description panel.")
        _append_ai_line("Please review and edit as needed, then SAVE to confirm.")
    elif "no" in reply:
        _append_ai_line("Understood. You can edit the Course Description manually at any time.")
    else:
        _append_ai_line("Confirm with YES or NO when you're ready for me to draft the description.")


def _handle_clos_reply(reply: str) -> None:
    followup = st.session_state.get("pcgs_ai_followup")

    if followup == "generate":
        if "yes" in reply:
            st.session_state["pcgs_clos"] = copy.deepcopy(CLO_PLACEHOLDERS)
            st.session_state["pcgs_ai_target_panel"] = Lex.CLO
            _ensure_min_clos()
            _sync_form_inputs()
            for idx, clo in enumerate(st.session_state["pcgs_clos"], start=1):
                _append_ai_line(f"CLO {idx} generated. {clo}")
            _append_ai_line("Is this satisfactory, or would you like me to try again?")
            st.session_state["pcgs_ai_followup"] = "review"
            return
        if "no" in reply:
            _append_ai_line("No problem. You can add your own CLOs in the Learning Objectives panel.")
            st.session_state["pcgs_ai_followup"] = None
            st.session_state["pcgs_ai_mode"] = "idle"
            return
        _append_ai_line("Respond with YES or NO so I know how to proceed.")
        return

    if followup == "review":
        if "no" in reply:
            st.session_state["pcgs_clos"] = copy.deepcopy(CLO_ALT_PLACEHOLDERS)
            st.session_state["pcgs_ai_target_panel"] = Lex.CLO
            _ensure_min_clos()
            _sync_form_inputs()
            _append_ai_line("Updated CLOs drafted. Let me know if you need another pass.")
        else:
            _append_ai_line("Great. Remember to SAVE once you're happy.")
        st.session_state["pcgs_ai_followup"] = None
        st.session_state["pcgs_ai_mode"] = "idle"
        return

    _append_ai_line("Engage the flame icon to start CLO drafting.")
    st.session_state["pcgs_ai_mode"] = "idle"


def _handle_manager_reply(mode: str) -> None:
    message = MANAGER_MESSAGES.get(mode, "PKE functionality for this area is coming soon.")
    stage = _mode_to_stage(mode)
    if stage:
        _set_ai_target(stage)
    _append_ai_line(message)


def _trigger_ai_prompt(target: str) -> None:
    stage = _mode_to_stage(target)
    st.session_state["pcgs_ai_mode"] = target
    st.session_state["pcgs_ai_followup"] = "generate" if target == "clos" else None
    _set_ai_target(stage)
    if stage in (Lex.SCALEMGR, Lex.CONTMGR, Lex.LSNMGR):
        _set_stage_complete(stage, True)
        _update_completion_flags()
    prompt = AI_PROMPTS.get(target)
    if prompt:
        _append_ai_line(prompt)


def _render_flame_button(target: str) -> None:
    st.markdown("<div class='pcgs-flame-button'>", unsafe_allow_html=True)
    if st.button(PKE_ICON, key=f"pcgs_flame_{target}", help="Engage PKE"):
        _trigger_ai_prompt(target)
    st.markdown("</div>", unsafe_allow_html=True)


def _append_ai_line(text: str) -> None:
    history = st.session_state["pcgs_ai_history"]
    history.append(("PKE", text))
    st.session_state["pcgs_ai_history"] = history[-HISTORY_LIMIT:]


def _append_user_line(text: str) -> None:
    history = st.session_state["pcgs_ai_history"]
    history.append(("USER", text))
    st.session_state["pcgs_ai_history"] = history[-HISTORY_LIMIT:]


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------


def _panel_classes(
    base: str,
    *,
    stage: Optional[Lex] = None,
    disabled: bool = False,
) -> str:
    classes = ["pcgs-panel", base]
    if disabled:
        classes.append("pcgs-panel--disabled")
    if stage is not None:
        if _stage_complete(stage):
            classes.append("pcgs-panel--complete")
        elif _has_unsaved_stage(stage):
            classes.append("pcgs-panel--unsaved")
        if _is_ai_highlight(stage):
            classes.append("pcgs-panel--ai-target")
    return " ".join(classes)


def _panel_status(stage: Lex) -> str:
    if _stage_complete(stage):
        return "ok"
    if _has_unsaved_stage(stage):
        return "warn"
    if _stage_has_content(stage):
        return "warn"
    return "idle"


def _stage_flag_key(stage: Lex) -> Optional[str]:
    return STEP_FLAG_KEYS.get(stage)


def _stage_complete(stage: Lex) -> bool:
    key = _stage_flag_key(stage)
    return bool(key and st.session_state.get(key))


def _set_stage_complete(stage: Lex, value: bool) -> None:
    key = _stage_flag_key(stage)
    if key:
        st.session_state[key] = value


def _has_unsaved_stage(stage: Lex) -> bool:
    snapshot = st.session_state["pcgs_saved_snapshot"]
    if stage == Lex.C_INFO:
        return st.session_state["pcgs_course_info"] != snapshot.get("course_info")
    if stage == Lex.C_DESC:
        return st.session_state["pcgs_course_description"] != snapshot.get("description")
    if stage == Lex.CLO:
        return st.session_state["pcgs_clos"] != snapshot.get("clos")
    return False


def _stage_has_content(stage: Lex) -> bool:
    if stage == Lex.C_INFO:
        info = st.session_state["pcgs_course_info"]
        return any(value.strip() for value in info.values())
    if stage == Lex.C_DESC:
        return bool(st.session_state["pcgs_course_description"].strip())
    if stage == Lex.CLO:
        return any(obj.strip() for obj in st.session_state["pcgs_clos"])
    return False


def _info_has_required_fields(info: Dict[Lex, str]) -> bool:
    required_fields = [
        Lex.C_NAME,
        Lex.C_LEVEL,
        Lex.C_THEME,
        Lex.C_DURATION,
        Lex.C_DEV,
    ]
    return all(info.get(field, "").strip() for field in required_fields)


def _update_completion_flags() -> None:
    saved = bool(st.session_state.get("pcgs_has_saved_once"))
    info = st.session_state["pcgs_course_info"]
    info_ready = _info_has_required_fields(info)
    _set_stage_complete(
        Lex.C_INFO,
        saved and info_ready and not _has_unsaved_stage(Lex.C_INFO),
    )

    description_ready = bool(st.session_state["pcgs_course_description"].strip())
    _set_stage_complete(
        Lex.C_DESC,
        saved and description_ready and not _has_unsaved_stage(Lex.C_DESC),
    )

    clos_ready = any(obj.strip() for obj in st.session_state["pcgs_clos"])
    _set_stage_complete(
        Lex.CLO,
        saved and clos_ready and not _has_unsaved_stage(Lex.CLO),
    )


def _connector_state(left: Lex, right: Lex) -> str:
    if _stage_complete(right):
        return "complete"
    if _stage_complete(left):
        return "active"
    return "idle"


def _get_next_stage() -> Optional[Lex]:
    for stage in COURSE_FLOW_SEQUENCE:
        if not _stage_complete(stage):
            return stage
    return None


def _tile_classes(stage: Lex) -> str:
    classes = ["pcgs-node-tile"]
    if _stage_complete(stage):
        classes.append("pcgs-node-tile--complete")
    elif _get_next_stage() == stage:
        classes.append("pcgs-node-tile--in-progress")
    else:
        classes.append("pcgs-node-tile--idle")
    if _is_ai_highlight(stage):
        classes.append("pcgs-node-tile--ai-target")
    return " ".join(classes)


def _mode_to_stage(mode: str) -> Optional[Lex]:
    return PKE_TARGET_TO_STAGE.get(mode)


def _set_ai_target(stage: Optional[Lex]) -> None:
    st.session_state["pcgs_ai_target_panel"] = stage
    if stage is not None:
        st.session_state["pcgs_ai_flash_panel"] = None
        st.session_state["pcgs_ai_flash_ticks"] = 0


def _flash_panel(stage: Lex) -> None:
    st.session_state["pcgs_ai_flash_panel"] = stage
    st.session_state["pcgs_ai_flash_ticks"] = 2


def _is_ai_highlight(stage: Lex) -> bool:
    flash_stage = st.session_state.get("pcgs_ai_flash_panel")
    flash_ticks = st.session_state.get("pcgs_ai_flash_ticks", 0)
    return (
        st.session_state.get("pcgs_ai_target_panel") == stage
        or (flash_stage == stage and flash_ticks > 0)
    )


def _tick_ai_flash() -> None:
    ticks = st.session_state.get("pcgs_ai_flash_ticks", 0)
    if ticks > 0:
        st.session_state["pcgs_ai_flash_ticks"] = ticks - 1
        if ticks - 1 == 0:
            st.session_state["pcgs_ai_flash_panel"] = None
    else:
        st.session_state["pcgs_ai_flash_panel"] = None


def _add_clo_row() -> None:
    st.session_state["pcgs_clos"].append("")
    _sync_form_inputs()


def _ensure_option(options: List[str], current: str) -> List[str]:
    if current and current not in options:
        return [current, *options]
    return options


def _sanitize(value: str) -> str:
    return html.escape(value)

