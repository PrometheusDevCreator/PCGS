"""
Authentication & Authorization Stubs

Defines placeholders for future user/session management. The legacy
Prometheus1 implementation handled authentication implicitly via Streamlit
session state; in v2 we will centralise role-based access controls and session
management within the app layer.
"""


def get_current_user():
    """
    Placeholder for retrieving the authenticated user context.
    """

    # TODO: Implement real session management using storage-backed user records
    # and secure authentication (password hashing, token handling, etc.).
    return None


def require_role(role: str) -> None:
    """
    Placeholder decorator/hook that will enforce role-based access.
    """

    # TODO: Re-implement the legacy "Admin vs Developer" restrictions with a
    # proper policy engine and audit logging.
    raise NotImplementedError("Authorization checks not yet implemented.")


