"""
PCGS Data Models

This module defines the core entities for the system as described in the Master Spec.
These models are used across the UI, Agents, and Export layers.

See Master Spec Section 6: Data Model Overview.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime

@dataclass
class User:
    """
    Represents a system user.
    See Spec 6.1.
    """
    id: str
    name: str
    email: str
    role: str  # 'Admin' or 'User'
    password_hash: str
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Lesson:
    """
    Represents a single lesson within a course.
    See Spec 6.1.
    """
    id: str
    course_id: str
    title: str
    duration_blocks: int = 1
    linked_scalar_items: List[str] = field(default_factory=list)
    content_sections: Dict[str, Any] = field(default_factory=dict)
    resources: List[str] = field(default_factory=list)
    assessment_items: List[str] = field(default_factory=list)

@dataclass
class Timetable:
    """
    Represents the schedule for a course.
    See Spec 6.1.
    """
    course_id: str
    # Placeholder for timetable structure (days, blocks, etc.)
    days: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Course:
    """
    Represents a training course.
    See Spec 6.1.
    """
    id: str
    name: str
    code: str
    duration_days: int
    thematic_area: str
    level: str
    developer_id: str  # Linked to User.id
    
    description: str = ""
    scalar: List[Dict[str, Any]] = field(default_factory=list) # List of objectives/structure items
    lessons: List[Lesson] = field(default_factory=list)
    timetable: Optional[Timetable] = None
    
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)







