"""
PCGS Application Layer Package

This package orchestrates the Prometheus Course Generation System (PCGS) app
experience. It provides facades around core entities, high-level workflows,
service integrations, and UI scaffolding so that future modules can grow
independently while remaining connected through clear interfaces.
"""

from . import core, logic, services, ui  # noqa: F401

__all__ = ["core", "logic", "services", "ui"]


