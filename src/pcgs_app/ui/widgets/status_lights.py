"""
Status Indicator Widgets

Reusable helpers for status dots/badges that align with the console theme.
"""

from typing import Literal

import streamlit as st

STATUS_CLASS_MAP = {
    "ok": "pcgs-status-dot pcgs-status-dot--ok",
    "warn": "pcgs-status-dot pcgs-status-dot--warn",
    "error": "pcgs-status-dot pcgs-status-dot--error",
    "idle": "pcgs-status-dot pcgs-status-dot--idle",
}


def render_status_dot(state: Literal["ok", "warn", "error", "idle"]) -> str:
    """
    Return the HTML span representing a themed status dot.
    """

    css_class = STATUS_CLASS_MAP.get(state, STATUS_CLASS_MAP["idle"])
    return f"<span class='{css_class}'></span>"


def render_status_light(label: str, status: str) -> None:
    """
    Retained for backwards compatibility with older prototypes.
    """

    dot = render_status_dot("ok" if status.lower() == "ready" else "idle")
    st.markdown(f"{dot} **{label}:** {status}", unsafe_allow_html=True)
