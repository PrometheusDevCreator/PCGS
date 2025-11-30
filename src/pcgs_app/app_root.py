"""
Application Root Orchestration

Provides centralized access to UI tab descriptors so Streamlit (or any other
front-end) can render the Prometheus experience without tightly coupling to
implementation details. In Phase 1 this simply returns placeholder tab
renderers; later it will coordinate state, routing, and permissions.
"""

from typing import Callable, Dict, List

from .ui.tabs import (
    tab_content,
    tab_create_course,
    tab_exports,
    tab_lessons,
    tab_planner,
    tab_scalar,
)

TabDescriptor = Dict[str, Callable[[], None]]


def get_app_tabs() -> List[TabDescriptor]:
    """
    Return the ordered list of tab descriptors for the Streamlit shell.

    Each descriptor defines:
    - id: stable identifier for routing/state
    - label: display label for the navigation widget
    - renderer: callable that knows how to render the tab
    """

    # TODO: Derive this list dynamically once navigation metadata is stored in
    # a configuration layer and permissions are enforced.
    return [
        {
            "id": "create",
            "label": "Create & Review",
            "renderer": tab_create_course.render_tab_create_course,
        },
        {
            "id": "scalar",
            "label": "Produce & Manage Scalar",
            "renderer": tab_scalar.render_tab_scalar,
        },
        {
            "id": "content",
            "label": "Manage Content",
            "renderer": tab_content.render_tab_content,
        },
        {
            "id": "lessons",
            "label": "Build Lessons",
            "renderer": tab_lessons.render_tab_lessons,
        },
        {
            "id": "planner",
            "label": "Planner",
            "renderer": tab_planner.render_tab_planner,
        },
        {
            "id": "exports",
            "label": "Generate Courseware",
            "renderer": tab_exports.render_tab_exports,
        },
    ]


