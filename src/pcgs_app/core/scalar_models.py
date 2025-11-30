"""
Scalar Data Models for Prometheus V2

Defines the canonical scalar structure for course content hierarchy:
- CLO (Course Learning Objective)
- Topic
- Subtopic
- Lesson
- Performance Criteria

Excel Template Contract:
------------------------
- Data begins at row 6
- Column B/C: CLO serial + text
- Column D/E: Topic serial + text
- Column F/G: Subtopic serial + text
- Column H/I: Lesson serial + text
- Column J/K: Performance Criteria serial + text

These models serialize to Dict for storage in Course.scalar (List[Dict[str, Any]])
to maintain compatibility with existing storage layer.
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Literal, Optional


class ScalarLevel(str, Enum):
    """
    Hierarchical levels within the course scalar.
    
    Order reflects the typical course structure:
    CLO → Topic → Subtopic → Lesson → Performance Criteria
    """
    CLO = "CLO"
    TOPIC = "Topic"
    SUBTOPIC = "Subtopic"
    LESSON = "Lesson"
    PERFORMANCE_CRITERIA = "PerformanceCriteria"


# Excel column mapping for each scalar level
# (serial_column, text_column) - 0-indexed from column A
EXCEL_COLUMN_MAP: Dict[ScalarLevel, tuple] = {
    ScalarLevel.CLO: (1, 2),                    # B, C
    ScalarLevel.TOPIC: (3, 4),                  # D, E
    ScalarLevel.SUBTOPIC: (5, 6),               # F, G
    ScalarLevel.LESSON: (7, 8),                 # H, I
    ScalarLevel.PERFORMANCE_CRITERIA: (9, 10),  # J, K
}

# Row where data starts (0-indexed, so row 6 = index 5)
EXCEL_DATA_START_ROW = 5


@dataclass
class ScalarEntry:
    """
    A single entry in the course scalar.
    
    Attributes:
        level: The hierarchical level (CLO, Topic, Subtopic, Lesson, PC)
        serial: The identifier/numbering (e.g., "1", "1.1", "1.1.1")
        text: The content/description text
        order_index: Position within entries of the same level (for UI ordering)
        parent_serial: Optional reference to parent entry's serial
        metadata: Optional additional data (e.g., Bloom's verb status)
    
    Serialization:
        Use to_dict() to convert for storage in Course.scalar
        Use from_dict() to reconstruct from stored data
    """
    level: ScalarLevel
    serial: str
    text: str
    order_index: int = 0
    parent_serial: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize to dictionary for storage in Course.scalar.
        
        Returns:
            Dict with all fields, level converted to string value.
        """
        return {
            "level": self.level.value,
            "serial": self.serial,
            "text": self.text,
            "order_index": self.order_index,
            "parent_serial": self.parent_serial,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ScalarEntry":
        """
        Reconstruct ScalarEntry from stored dictionary.
        
        Args:
            data: Dictionary from Course.scalar storage
            
        Returns:
            ScalarEntry instance
        """
        level_value = data.get("level", "CLO")
        try:
            level = ScalarLevel(level_value)
        except ValueError:
            # Fallback for legacy data
            level = ScalarLevel.CLO
        
        return cls(
            level=level,
            serial=data.get("serial", ""),
            text=data.get("text", ""),
            order_index=data.get("order_index", 0),
            parent_serial=data.get("parent_serial"),
            metadata=data.get("metadata", {}),
        )
    
    def __str__(self) -> str:
        return f"{self.serial}: {self.text[:50]}..." if len(self.text) > 50 else f"{self.serial}: {self.text}"


@dataclass
class ScalarCollection:
    """
    Container for all scalar entries in a course, organized by level.
    
    Provides convenience methods for:
    - Accessing entries by level
    - Counting entries per level
    - Serializing/deserializing the full scalar
    - Auto-renumbering after modifications
    """
    entries: List[ScalarEntry] = field(default_factory=list)
    
    def get_by_level(self, level: ScalarLevel) -> List[ScalarEntry]:
        """Get all entries for a specific level, sorted by order_index."""
        return sorted(
            [e for e in self.entries if e.level == level],
            key=lambda e: e.order_index
        )
    
    def count_by_level(self, level: ScalarLevel) -> int:
        """Count entries for a specific level."""
        return len([e for e in self.entries if e.level == level])
    
    def get_counts(self) -> Dict[ScalarLevel, int]:
        """Get counts for all levels."""
        return {level: self.count_by_level(level) for level in ScalarLevel}
    
    def add_entry(self, entry: ScalarEntry) -> None:
        """
        Add an entry, auto-assigning order_index if not set.
        """
        if entry.order_index == 0:
            level_entries = self.get_by_level(entry.level)
            entry.order_index = len(level_entries) + 1
        self.entries.append(entry)
    
    def remove_entry(self, level: ScalarLevel, serial: str) -> bool:
        """
        Remove an entry by level and serial.
        
        Returns:
            True if entry was found and removed, False otherwise.
        """
        for i, entry in enumerate(self.entries):
            if entry.level == level and entry.serial == serial:
                self.entries.pop(i)
                return True
        return False
    
    def update_entry(self, level: ScalarLevel, serial: str, 
                     new_serial: Optional[str] = None, 
                     new_text: Optional[str] = None) -> bool:
        """
        Update an entry's serial and/or text.
        
        Returns:
            True if entry was found and updated, False otherwise.
        """
        for entry in self.entries:
            if entry.level == level and entry.serial == serial:
                if new_serial is not None:
                    entry.serial = new_serial
                if new_text is not None:
                    entry.text = new_text
                return True
        return False
    
    def reorder_level(self, level: ScalarLevel, serials_in_order: List[str]) -> None:
        """
        Reorder entries of a level based on the provided serial order.
        Updates order_index for each entry.
        
        Args:
            level: The level to reorder
            serials_in_order: List of serials in the desired order
        """
        level_entries = {e.serial: e for e in self.entries if e.level == level}
        for idx, serial in enumerate(serials_in_order, start=1):
            if serial in level_entries:
                level_entries[serial].order_index = idx
    
    def renumber_level(self, level: ScalarLevel, prefix: str = "") -> None:
        """
        Auto-renumber all entries of a level sequentially.
        
        Args:
            level: The level to renumber
            prefix: Optional prefix for serial (e.g., "1." for topics under CLO 1)
        
        Renumbering rules:
        - CLOs: 1, 2, 3, ...
        - Topics: 1.1, 1.2, ... (if prefix="1.")
        - Or simple: 1, 2, 3 if no prefix
        """
        level_entries = self.get_by_level(level)
        for idx, entry in enumerate(level_entries, start=1):
            if prefix:
                entry.serial = f"{prefix}{idx}"
            else:
                entry.serial = str(idx)
            entry.order_index = idx
    
    def to_list(self) -> List[Dict[str, Any]]:
        """
        Serialize all entries to list of dicts for Course.scalar storage.
        """
        return [entry.to_dict() for entry in self.entries]
    
    @classmethod
    def from_list(cls, data: List[Dict[str, Any]]) -> "ScalarCollection":
        """
        Reconstruct ScalarCollection from Course.scalar storage.
        """
        entries = [ScalarEntry.from_dict(d) for d in data]
        return cls(entries=entries)
    
    def clear(self) -> None:
        """Clear all entries."""
        self.entries.clear()
    
    def clear_level(self, level: ScalarLevel) -> None:
        """Clear all entries of a specific level."""
        self.entries = [e for e in self.entries if e.level != level]


# Bloom's Taxonomy verbs for CLO validation
# These are commonly accepted performance verbs at various cognitive levels
BLOOMS_VERBS = {
    # Remember
    "DEFINE", "DESCRIBE", "IDENTIFY", "LABEL", "LIST", "MATCH", "NAME",
    "OUTLINE", "RECALL", "RECOGNIZE", "REPRODUCE", "SELECT", "STATE",
    
    # Understand
    "CLASSIFY", "COMPARE", "CONTRAST", "DEMONSTRATE", "DISCUSS",
    "DISTINGUISH", "ESTIMATE", "EXPLAIN", "EXTEND", "ILLUSTRATE",
    "INTERPRET", "PARAPHRASE", "PREDICT", "SUMMARIZE",
    
    # Apply
    "APPLY", "CALCULATE", "CHANGE", "COMPLETE", "COMPUTE", "CONSTRUCT",
    "DRAMATIZE", "EMPLOY", "EXAMINE", "EXECUTE", "IMPLEMENT", "MODIFY",
    "OPERATE", "PRACTICE", "PREPARE", "PRODUCE", "SCHEDULE", "SHOW",
    "SKETCH", "SOLVE", "USE",
    
    # Analyze
    "ANALYSE", "ANALYZE", "APPRAISE", "BREAKDOWN", "CATEGORIZE",
    "CRITICIZE", "DEBATE", "DIAGRAM", "DIFFERENTIATE", "DISCRIMINATE",
    "EXAMINE", "EXPERIMENT", "INFER", "INSPECT", "INVESTIGATE",
    "ORGANIZE", "QUESTION", "RELATE", "RESEARCH", "SEPARATE", "TEST",
    
    # Evaluate
    "APPRAISE", "ARGUE", "ASSESS", "CHOOSE", "CONCLUDE", "CRITIQUE",
    "DECIDE", "DEFEND", "EVALUATE", "JUDGE", "JUSTIFY", "MEASURE",
    "PRIORITIZE", "RANK", "RATE", "RECOMMEND", "REVIEW", "SCORE",
    "SELECT", "SUPPORT", "VALIDATE", "VALUE", "VERIFY",
    
    # Create
    "ARRANGE", "ASSEMBLE", "BUILD", "COMBINE", "COMPOSE", "CONSTRUCT",
    "CREATE", "DESIGN", "DEVELOP", "DEVISE", "FORMULATE", "GENERATE",
    "HYPOTHESIZE", "INTEGRATE", "INVENT", "MAKE", "ORIGINATE", "PLAN",
    "PRODUCE", "PROPOSE", "REARRANGE", "RECONSTRUCT", "REORGANIZE",
    "REVISE", "REWRITE", "SYNTHESIZE", "WRITE",
}


def check_blooms_verb(text: str) -> tuple:
    """
    Check if text starts with a Bloom's Taxonomy verb.
    
    Args:
        text: The CLO text to check
        
    Returns:
        Tuple of (has_verb: bool, verb: str or None, corrected_text: str)
        - has_verb: True if a Bloom's verb is found at the start
        - verb: The detected verb (uppercase) or None
        - corrected_text: Text with the verb capitalized if found
    """
    if not text or not text.strip():
        return (False, None, text)
    
    words = text.strip().split()
    if not words:
        return (False, None, text)
    
    first_word = words[0].upper().rstrip(".,;:")
    
    if first_word in BLOOMS_VERBS:
        # Capitalize the verb and reconstruct text
        corrected = first_word.capitalize() + text[len(words[0]):]
        return (True, first_word, corrected)
    
    return (False, None, text)

