"""
Scalar Service Tests

Tests for the scalar data models and service layer:
- ScalarEntry and ScalarCollection operations
- CRUD operations (add, update, delete, reorder)
- Bloom's verb validation for CLOs
- Excel import (mock data)
"""

import sys
import os
import pytest

# Add src to path for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from pcgs_app.core.scalar_models import (
    ScalarEntry,
    ScalarLevel,
    ScalarCollection,
    BLOOMS_VERBS,
    check_blooms_verb,
)


# ============================================================================
# ScalarEntry Tests
# ============================================================================

class TestScalarEntry:
    """Tests for ScalarEntry dataclass."""
    
    def test_create_entry(self):
        """Test basic entry creation."""
        entry = ScalarEntry(
            level=ScalarLevel.CLO,
            serial="1",
            text="Identify security threats",
            order_index=1,
        )
        assert entry.level == ScalarLevel.CLO
        assert entry.serial == "1"
        assert entry.text == "Identify security threats"
        assert entry.order_index == 1
        assert entry.parent_serial is None
        assert entry.metadata == {}
    
    def test_to_dict(self):
        """Test serialization to dictionary."""
        entry = ScalarEntry(
            level=ScalarLevel.TOPIC,
            serial="1.1",
            text="Network Security",
            order_index=1,
        )
        d = entry.to_dict()
        
        assert d["level"] == "Topic"
        assert d["serial"] == "1.1"
        assert d["text"] == "Network Security"
        assert d["order_index"] == 1
    
    def test_from_dict(self):
        """Test deserialization from dictionary."""
        data = {
            "level": "CLO",
            "serial": "2",
            "text": "Analyze network traffic",
            "order_index": 2,
            "parent_serial": None,
            "metadata": {"blooms_valid": True},
        }
        entry = ScalarEntry.from_dict(data)
        
        assert entry.level == ScalarLevel.CLO
        assert entry.serial == "2"
        assert entry.text == "Analyze network traffic"
        assert entry.metadata.get("blooms_valid") is True
    
    def test_from_dict_invalid_level(self):
        """Test fallback for invalid level value."""
        data = {
            "level": "InvalidLevel",
            "serial": "1",
            "text": "Test",
        }
        entry = ScalarEntry.from_dict(data)
        assert entry.level == ScalarLevel.CLO  # Fallback
    
    def test_str_representation(self):
        """Test string representation."""
        entry = ScalarEntry(
            level=ScalarLevel.CLO,
            serial="1",
            text="This is a very long text that should be truncated in the string representation",
        )
        str_repr = str(entry)
        assert "1:" in str_repr
        assert "..." in str_repr


# ============================================================================
# ScalarCollection Tests
# ============================================================================

class TestScalarCollection:
    """Tests for ScalarCollection container."""
    
    def test_empty_collection(self):
        """Test empty collection initialization."""
        collection = ScalarCollection()
        assert len(collection.entries) == 0
        assert collection.count_by_level(ScalarLevel.CLO) == 0
    
    def test_add_entry(self):
        """Test adding entries to collection."""
        collection = ScalarCollection()
        
        entry1 = ScalarEntry(ScalarLevel.CLO, "1", "First CLO")
        entry2 = ScalarEntry(ScalarLevel.CLO, "2", "Second CLO")
        
        collection.add_entry(entry1)
        collection.add_entry(entry2)
        
        assert collection.count_by_level(ScalarLevel.CLO) == 2
        assert collection.count_by_level(ScalarLevel.TOPIC) == 0
    
    def test_auto_order_index(self):
        """Test auto-assignment of order_index."""
        collection = ScalarCollection()
        
        entry1 = ScalarEntry(ScalarLevel.CLO, "1", "First CLO", order_index=0)
        entry2 = ScalarEntry(ScalarLevel.CLO, "2", "Second CLO", order_index=0)
        
        collection.add_entry(entry1)
        collection.add_entry(entry2)
        
        clos = collection.get_by_level(ScalarLevel.CLO)
        assert clos[0].order_index == 1
        assert clos[1].order_index == 2
    
    def test_get_by_level(self):
        """Test filtering entries by level."""
        collection = ScalarCollection()
        collection.add_entry(ScalarEntry(ScalarLevel.CLO, "1", "CLO 1"))
        collection.add_entry(ScalarEntry(ScalarLevel.TOPIC, "1.1", "Topic 1"))
        collection.add_entry(ScalarEntry(ScalarLevel.CLO, "2", "CLO 2"))
        
        clos = collection.get_by_level(ScalarLevel.CLO)
        topics = collection.get_by_level(ScalarLevel.TOPIC)
        
        assert len(clos) == 2
        assert len(topics) == 1
    
    def test_remove_entry(self):
        """Test removing entries."""
        collection = ScalarCollection()
        collection.add_entry(ScalarEntry(ScalarLevel.CLO, "1", "CLO 1"))
        collection.add_entry(ScalarEntry(ScalarLevel.CLO, "2", "CLO 2"))
        
        result = collection.remove_entry(ScalarLevel.CLO, "1")
        
        assert result is True
        assert collection.count_by_level(ScalarLevel.CLO) == 1
        assert collection.get_by_level(ScalarLevel.CLO)[0].serial == "2"
    
    def test_remove_nonexistent_entry(self):
        """Test removing non-existent entry returns False."""
        collection = ScalarCollection()
        result = collection.remove_entry(ScalarLevel.CLO, "999")
        assert result is False
    
    def test_update_entry(self):
        """Test updating entry fields."""
        collection = ScalarCollection()
        collection.add_entry(ScalarEntry(ScalarLevel.CLO, "1", "Original text"))
        
        result = collection.update_entry(
            ScalarLevel.CLO, "1",
            new_serial="CLO-1",
            new_text="Updated text"
        )
        
        assert result is True
        entry = collection.get_by_level(ScalarLevel.CLO)[0]
        assert entry.serial == "CLO-1"
        assert entry.text == "Updated text"
    
    def test_renumber_level(self):
        """Test renumbering entries in a level."""
        collection = ScalarCollection()
        collection.add_entry(ScalarEntry(ScalarLevel.CLO, "A", "First", order_index=1))
        collection.add_entry(ScalarEntry(ScalarLevel.CLO, "B", "Second", order_index=2))
        collection.add_entry(ScalarEntry(ScalarLevel.CLO, "C", "Third", order_index=3))
        
        collection.renumber_level(ScalarLevel.CLO)
        
        clos = collection.get_by_level(ScalarLevel.CLO)
        serials = [c.serial for c in clos]
        assert serials == ["1", "2", "3"]
    
    def test_renumber_with_prefix(self):
        """Test renumbering with prefix."""
        collection = ScalarCollection()
        collection.add_entry(ScalarEntry(ScalarLevel.TOPIC, "A", "First", order_index=1))
        collection.add_entry(ScalarEntry(ScalarLevel.TOPIC, "B", "Second", order_index=2))
        
        collection.renumber_level(ScalarLevel.TOPIC, prefix="1.")
        
        topics = collection.get_by_level(ScalarLevel.TOPIC)
        serials = [t.serial for t in topics]
        assert serials == ["1.1", "1.2"]
    
    def test_reorder_level(self):
        """Test reordering entries by serial list."""
        collection = ScalarCollection()
        collection.add_entry(ScalarEntry(ScalarLevel.CLO, "1", "First", order_index=1))
        collection.add_entry(ScalarEntry(ScalarLevel.CLO, "2", "Second", order_index=2))
        collection.add_entry(ScalarEntry(ScalarLevel.CLO, "3", "Third", order_index=3))
        
        # Reverse order
        collection.reorder_level(ScalarLevel.CLO, ["3", "2", "1"])
        
        clos = collection.get_by_level(ScalarLevel.CLO)
        assert clos[0].serial == "3"
        assert clos[1].serial == "2"
        assert clos[2].serial == "1"
    
    def test_to_list_from_list(self):
        """Test serialization round-trip."""
        collection = ScalarCollection()
        collection.add_entry(ScalarEntry(ScalarLevel.CLO, "1", "CLO 1"))
        collection.add_entry(ScalarEntry(ScalarLevel.TOPIC, "1.1", "Topic 1"))
        
        data = collection.to_list()
        restored = ScalarCollection.from_list(data)
        
        assert restored.count_by_level(ScalarLevel.CLO) == 1
        assert restored.count_by_level(ScalarLevel.TOPIC) == 1
    
    def test_clear(self):
        """Test clearing all entries."""
        collection = ScalarCollection()
        collection.add_entry(ScalarEntry(ScalarLevel.CLO, "1", "CLO 1"))
        collection.add_entry(ScalarEntry(ScalarLevel.TOPIC, "1.1", "Topic 1"))
        
        collection.clear()
        
        assert len(collection.entries) == 0
    
    def test_clear_level(self):
        """Test clearing entries of a specific level."""
        collection = ScalarCollection()
        collection.add_entry(ScalarEntry(ScalarLevel.CLO, "1", "CLO 1"))
        collection.add_entry(ScalarEntry(ScalarLevel.TOPIC, "1.1", "Topic 1"))
        
        collection.clear_level(ScalarLevel.CLO)
        
        assert collection.count_by_level(ScalarLevel.CLO) == 0
        assert collection.count_by_level(ScalarLevel.TOPIC) == 1
    
    def test_get_counts(self):
        """Test getting counts for all levels."""
        collection = ScalarCollection()
        collection.add_entry(ScalarEntry(ScalarLevel.CLO, "1", "CLO 1"))
        collection.add_entry(ScalarEntry(ScalarLevel.CLO, "2", "CLO 2"))
        collection.add_entry(ScalarEntry(ScalarLevel.TOPIC, "1.1", "Topic 1"))
        
        counts = collection.get_counts()
        
        assert counts[ScalarLevel.CLO] == 2
        assert counts[ScalarLevel.TOPIC] == 1
        assert counts[ScalarLevel.SUBTOPIC] == 0


# ============================================================================
# Bloom's Verb Validation Tests
# ============================================================================

class TestBloomsValidation:
    """Tests for Bloom's Taxonomy verb validation."""
    
    def test_blooms_verbs_exist(self):
        """Test that Bloom's verbs set is populated."""
        assert len(BLOOMS_VERBS) > 50
        assert "IDENTIFY" in BLOOMS_VERBS
        assert "ANALYZE" in BLOOMS_VERBS
        assert "EVALUATE" in BLOOMS_VERBS
        assert "CREATE" in BLOOMS_VERBS
    
    def test_check_blooms_verb_valid(self):
        """Test detection of valid Bloom's verb."""
        has_verb, verb, corrected = check_blooms_verb("identify security threats")
        
        assert has_verb is True
        assert verb == "IDENTIFY"
        assert corrected.startswith("Identify")
    
    def test_check_blooms_verb_uppercase(self):
        """Test detection with uppercase verb."""
        has_verb, verb, corrected = check_blooms_verb("ANALYZE network traffic")
        
        assert has_verb is True
        assert verb == "ANALYZE"
    
    def test_check_blooms_verb_invalid(self):
        """Test detection when no Bloom's verb present."""
        has_verb, verb, corrected = check_blooms_verb("Learn about security")
        
        assert has_verb is False
        assert verb is None
        assert corrected == "Learn about security"
    
    def test_check_blooms_verb_empty(self):
        """Test handling of empty text."""
        has_verb, verb, corrected = check_blooms_verb("")
        
        assert has_verb is False
        assert verb is None
    
    def test_check_blooms_verb_with_punctuation(self):
        """Test handling of verb with trailing punctuation."""
        has_verb, verb, corrected = check_blooms_verb("Describe: the main concepts")
        
        assert has_verb is True
        assert verb == "DESCRIBE"
    
    def test_various_blooms_verbs(self):
        """Test various Bloom's verbs across cognitive levels."""
        test_cases = [
            ("Define the term", True, "DEFINE"),
            ("Explain the process", True, "EXPLAIN"),
            ("Apply the formula", True, "APPLY"),
            ("Evaluate the results", True, "EVALUATE"),
            ("Design a solution", True, "DESIGN"),
            ("Understand the concept", False, None),  # Not a Bloom's verb
        ]
        
        for text, expected_valid, expected_verb in test_cases:
            has_verb, verb, _ = check_blooms_verb(text)
            assert has_verb == expected_valid, f"Failed for: {text}"
            assert verb == expected_verb, f"Failed for: {text}"


# ============================================================================
# Integration Tests
# ============================================================================

class TestScalarIntegration:
    """Integration tests for scalar workflow."""
    
    def test_full_workflow(self):
        """Test complete add-update-delete workflow."""
        collection = ScalarCollection()
        
        # Add entries
        collection.add_entry(ScalarEntry(ScalarLevel.CLO, "1", "Identify threats"))
        collection.add_entry(ScalarEntry(ScalarLevel.CLO, "2", "Analyze patterns"))
        collection.add_entry(ScalarEntry(ScalarLevel.TOPIC, "1.1", "Network threats"))
        
        assert collection.count_by_level(ScalarLevel.CLO) == 2
        
        # Update entry
        collection.update_entry(ScalarLevel.CLO, "1", new_text="Identify security threats")
        clo1 = collection.get_by_level(ScalarLevel.CLO)[0]
        assert "security" in clo1.text
        
        # Delete entry
        collection.remove_entry(ScalarLevel.CLO, "2")
        assert collection.count_by_level(ScalarLevel.CLO) == 1
        
        # Renumber
        collection.renumber_level(ScalarLevel.CLO)
        clo = collection.get_by_level(ScalarLevel.CLO)[0]
        assert clo.serial == "1"
    
    def test_hierarchical_structure(self):
        """Test building a hierarchical course structure."""
        collection = ScalarCollection()
        
        # Build structure
        collection.add_entry(ScalarEntry(ScalarLevel.CLO, "1", "Master network security"))
        collection.add_entry(ScalarEntry(ScalarLevel.TOPIC, "1.1", "Firewalls", parent_serial="1"))
        collection.add_entry(ScalarEntry(ScalarLevel.SUBTOPIC, "1.1.1", "Types of firewalls", parent_serial="1.1"))
        collection.add_entry(ScalarEntry(ScalarLevel.LESSON, "L1", "Introduction to firewalls"))
        collection.add_entry(ScalarEntry(ScalarLevel.PERFORMANCE_CRITERIA, "PC1", "Configure firewall rules"))
        
        # Verify structure
        counts = collection.get_counts()
        assert counts[ScalarLevel.CLO] == 1
        assert counts[ScalarLevel.TOPIC] == 1
        assert counts[ScalarLevel.SUBTOPIC] == 1
        assert counts[ScalarLevel.LESSON] == 1
        assert counts[ScalarLevel.PERFORMANCE_CRITERIA] == 1
        
        # Serialize and restore
        data = collection.to_list()
        assert len(data) == 5
        
        restored = ScalarCollection.from_list(data)
        assert restored.count_by_level(ScalarLevel.CLO) == 1

