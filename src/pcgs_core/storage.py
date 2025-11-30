"""
PCGS Storage Interface

Defines the abstract interface for data persistence.
Implementations (local JSON, SQLite, etc.) should follow this contract.
"""

from typing import List, Optional
from .models import Course, User

# Placeholder for storage implementation
# In Phase 2, this will be fleshed out with actual file/DB handling.

def save_course(course: Course) -> None:
    """
    Save a course object to storage.
    """
    # TODO: Implement persistence
    print(f"[STORAGE] Would save course: {course.name} ({course.id})")
    # raise NotImplementedError("Storage implementation pending")

def load_course(course_id: str) -> Optional[Course]:
    """
    Load a course by ID.
    """
    # TODO: Implement retrieval
    print(f"[STORAGE] Would load course: {course_id}")
    return None

def list_courses(user_id: str) -> List[Course]:
    """
    List all courses for a specific user.
    """
    # TODO: Implement listing
    print(f"[STORAGE] Would list courses for user: {user_id}")
    return []







