"""
PKE Client Stub

Defines the surface that will interface with OpenAI/Anthropic/Gemini (or any
other LLM). For now this simply proxies to the placeholder pcgs_agents module.
"""

from typing import Any, Dict, List

from pcgs_agents import pke as legacy_pke


def generate_course_description(brief: Dict[str, Any]) -> str:
    """
    Proxy to the legacy placeholder until the new client is implemented.
    """

    # TODO: Replace with real client implementation (API routing, retries,
    # logging, guardrails).
    return legacy_pke.generate_course_description(brief)


def generate_scalar(brief: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Proxy for scalar generation.
    """

    # TODO: Add deterministic scaffolding, caching, and validation.
    return legacy_pke.generate_scalar(brief)


def generate_lessons(course_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Proxy for lesson generation.
    """

    # TODO: Support multi-pass prompting and structured outputs.
    return legacy_pke.generate_lessons(course_data)


