"""
Application Core Facade

Re-exports foundational PCGS entities so upper layers can import from
`pcgs_app.core` while `pcgs_core` continues to house the concrete
implementation. Over time the app layer can introduce adapters, validators,
and compatibility helpers without forcing the UI or services to refactor.
"""

from pcgs_core import __version__  # noqa: F401

from . import config, models, storage  # noqa: F401

__all__ = ["__version__", "config", "models", "storage"]


