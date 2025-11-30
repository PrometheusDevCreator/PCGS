"""
High-Level Workflow Orchestrators

Provides a future-safe location for application workflows that coordinate
between UI inputs, validations, storage, and the core engine. These functions
will eventually replace the monolithic Streamlit handlers from Prometheus1.
"""

from typing import Any, Dict

from pcgs_core import workflows as core_workflows


def create_course(user_id: str, course_data: Dict[str, Any]):
    """
    Wrap the core workflow with upcoming validation, auditing, and state hooks.
    """

    # TODO: Inject validators, lexicon enrichment, and persistence events.
    return core_workflows.create_new_course(user_id=user_id, course_data=course_data)


def generate_scalar(course) -> None:
    """
    Coordinate scalar generation (manual + PKE) for a course object.
    """

    # TODO: Re-implement legacy scalar builder flow with deterministic state
    # transitions and template-backed exports.
    return core_workflows.build_scalar_for_course(course=course)


def generate_lessons(course) -> None:
    """
    Coordinate lesson generation plus downstream planner/export hooks.
    """

    # TODO: Add batching, PKE retries, and user overrides.
    return core_workflows.build_lessons_for_course(course=course)


def generate_timetable(course) -> None:
    """
    Prepare the timetable/planner structures for exports.
    """

    # TODO: Port the legacy planner logic (lesson sequencing, Rabdan day plan)
    # into a reusable scheduling service.
    return core_workflows.build_timetable_for_course(course=course)


