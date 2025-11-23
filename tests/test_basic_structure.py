"""
Basic Structure Test

Verifies that the project skeleton is set up correctly and imports work.
"""

import sys
import os
import pytest

# Add src to path for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from pcgs_core.models import Course, User
from pcgs_core.config import load_config
from pcgs_agents.pke import generate_course_description

def test_models_exist():
    """Test that core models can be instantiated."""
    user = User(id="u1", name="Test User", email="test@example.com", role="Admin", password_hash="hash")
    assert user.name == "Test User"
    
    course = Course(
        id="c1", 
        name="Test Course", 
        code="TC101", 
        duration_days=5, 
        thematic_area="IT", 
        level="Basic", 
        developer_id=user.id
    )
    assert course.code == "TC101"
    assert course.developer_id == "u1"

def test_config_loads():
    """Test that configuration loads."""
    config = load_config()
    assert config.APP_NAME == "PCGS v2"

def test_agent_interface_exists():
    """Test that agent placeholder functions exist."""
    desc = generate_course_description({})
    assert isinstance(desc, str)
    assert "placeholder" in desc

