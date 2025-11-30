"""
Configuration Facade

Wraps `pcgs_core.config` so application modules can import from the app layer
while the underlying implementation remains in the core package. Future
enhancements (theme selection, workspace contexts) can hook in here without
modifying the lower-level config module immediately.
"""

from pcgs_core.config import Config, load_config  # noqa: F401

__all__ = ["Config", "load_config"]


