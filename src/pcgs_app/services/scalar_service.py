"""
Scalar Service for Prometheus V2

Central service layer for all scalar operations:
- Excel import (from template)
- CRUD operations (add, update, delete)
- Reordering and renumbering
- Bloom's verb validation for CLOs
- Session state management for UI

This is the single source of truth for scalar data manipulation.
The UI layer should call these functions rather than manipulating
scalar data directly.
"""

from typing import Any, Dict, List, Optional, Tuple
import streamlit as st

from pcgs_app.core.scalar_models import (
    ScalarEntry,
    ScalarLevel,
    ScalarCollection,
    EXCEL_COLUMN_MAP,
    EXCEL_DATA_START_ROW,
    BLOOMS_VERBS,
    check_blooms_verb,
)


# Session state keys for scalar management
SCALAR_STATE_KEY = "pcgs_scalar_collection"
SCALAR_WARNINGS_KEY = "pcgs_scalar_warnings"
SCALAR_DIRTY_KEY = "pcgs_scalar_dirty"  # True if unsaved changes exist


# ============================================================================
# Session State Management
# ============================================================================

def init_scalar_state() -> None:
    """
    Initialize scalar-related session state.
    Call this at the start of the scalar tab render.
    """
    if SCALAR_STATE_KEY not in st.session_state:
        st.session_state[SCALAR_STATE_KEY] = ScalarCollection()
    if SCALAR_WARNINGS_KEY not in st.session_state:
        st.session_state[SCALAR_WARNINGS_KEY] = []
    if SCALAR_DIRTY_KEY not in st.session_state:
        st.session_state[SCALAR_DIRTY_KEY] = False


def get_scalar_collection() -> ScalarCollection:
    """
    Get the current scalar collection from session state.
    
    Returns:
        ScalarCollection instance
    """
    init_scalar_state()
    return st.session_state[SCALAR_STATE_KEY]


def set_scalar_collection(collection: ScalarCollection) -> None:
    """
    Set the scalar collection in session state.
    
    Args:
        collection: ScalarCollection to store
    """
    st.session_state[SCALAR_STATE_KEY] = collection
    st.session_state[SCALAR_DIRTY_KEY] = True


def get_warnings() -> List[str]:
    """Get current warnings list."""
    init_scalar_state()
    return st.session_state[SCALAR_WARNINGS_KEY]


def add_warning(message: str) -> None:
    """Add a warning message."""
    init_scalar_state()
    warnings = st.session_state[SCALAR_WARNINGS_KEY]
    if message not in warnings:
        warnings.append(message)
    # Keep only last 10 warnings
    st.session_state[SCALAR_WARNINGS_KEY] = warnings[-10:]


def clear_warnings() -> None:
    """Clear all warnings."""
    st.session_state[SCALAR_WARNINGS_KEY] = []


def is_dirty() -> bool:
    """Check if there are unsaved changes."""
    init_scalar_state()
    return st.session_state.get(SCALAR_DIRTY_KEY, False)


def mark_clean() -> None:
    """Mark scalar as saved (no unsaved changes)."""
    st.session_state[SCALAR_DIRTY_KEY] = False


def mark_dirty() -> None:
    """Mark scalar as having unsaved changes."""
    st.session_state[SCALAR_DIRTY_KEY] = True


# ============================================================================
# Excel Import
# ============================================================================

def import_scalar_from_excel(file_content: bytes) -> Tuple[bool, str, ScalarCollection]:
    """
    Import scalar data from Excel file content.
    
    Excel Template Contract:
    - Data begins at row 6 (index 5)
    - Column B/C: CLO serial + text
    - Column D/E: Topic serial + text
    - Column F/G: Subtopic serial + text
    - Column H/I: Lesson serial + text
    - Column J/K: Performance Criteria serial + text
    
    Args:
        file_content: Raw bytes from uploaded Excel file
        
    Returns:
        Tuple of (success: bool, message: str, collection: ScalarCollection)
    """
    try:
        import openpyxl
        from io import BytesIO
    except ImportError:
        return (False, "openpyxl library not installed. Run: pip install openpyxl", ScalarCollection())
    
    try:
        # Load workbook from bytes
        workbook = openpyxl.load_workbook(BytesIO(file_content), data_only=True)
        sheet = workbook.active
        
        if sheet is None:
            return (False, "No active sheet found in workbook", ScalarCollection())
        
        collection = ScalarCollection()
        counts = {level: 0 for level in ScalarLevel}
        
        # Process rows starting from row 6 (index 5)
        for row_idx, row in enumerate(sheet.iter_rows(min_row=EXCEL_DATA_START_ROW + 1), start=1):
            # Process each scalar level
            for level, (serial_col, text_col) in EXCEL_COLUMN_MAP.items():
                serial_cell = row[serial_col] if serial_col < len(row) else None
                text_cell = row[text_col] if text_col < len(row) else None
                
                serial = str(serial_cell.value).strip() if serial_cell and serial_cell.value else ""
                text = str(text_cell.value).strip() if text_cell and text_cell.value else ""
                
                # Only add if we have meaningful content
                if serial or text:
                    counts[level] += 1
                    entry = ScalarEntry(
                        level=level,
                        serial=serial or str(counts[level]),
                        text=text,
                        order_index=counts[level],
                    )
                    collection.add_entry(entry)
        
        # Generate summary
        total = sum(counts.values())
        summary_parts = [f"{counts[level]} {level.value}s" for level in ScalarLevel if counts[level] > 0]
        summary = f"Imported {total} entries: " + ", ".join(summary_parts)
        
        # Validate CLOs for Bloom's verbs
        validate_all_clos(collection)
        
        return (True, summary, collection)
        
    except Exception as e:
        return (False, f"Error reading Excel file: {str(e)}", ScalarCollection())


def import_scalar_from_file(uploaded_file) -> Tuple[bool, str]:
    """
    Import scalar from Streamlit uploaded file object.
    Updates session state directly.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    if uploaded_file is None:
        return (False, "No file uploaded")
    
    try:
        content = uploaded_file.read()
        success, message, collection = import_scalar_from_excel(content)
        
        if success:
            set_scalar_collection(collection)
            mark_dirty()
        
        return (success, message)
        
    except Exception as e:
        return (False, f"Error processing file: {str(e)}")


# ============================================================================
# CRUD Operations
# ============================================================================

def add_scalar_entry(level: ScalarLevel, serial: str, text: str, 
                     auto_number: bool = True) -> Tuple[bool, str]:
    """
    Add a new scalar entry.
    
    Args:
        level: The scalar level (CLO, Topic, etc.)
        serial: The serial/identifier (can be empty if auto_number=True)
        text: The content text
        auto_number: If True and serial is empty, auto-assign next number
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    collection = get_scalar_collection()
    
    # Auto-number if serial is empty
    if auto_number and not serial.strip():
        count = collection.count_by_level(level)
        serial = str(count + 1)
    
    if not serial.strip():
        return (False, "Serial number is required")
    
    if not text.strip():
        return (False, "Text content is required")
    
    # Check for duplicate serial within same level
    existing = collection.get_by_level(level)
    if any(e.serial == serial for e in existing):
        return (False, f"Serial '{serial}' already exists for {level.value}")
    
    entry = ScalarEntry(
        level=level,
        serial=serial.strip(),
        text=text.strip(),
        order_index=len(existing) + 1,
    )
    
    # Validate Bloom's verb for CLOs
    if level == ScalarLevel.CLO:
        has_verb, verb, corrected = check_blooms_verb(text)
        entry.text = corrected
        if not has_verb:
            add_warning(f"Warning: CLO {serial} does not start with a Bloom's performance verb.")
    
    collection.add_entry(entry)
    mark_dirty()
    
    return (True, f"Added {level.value}: {serial}")


def update_scalar_entry(level: ScalarLevel, old_serial: str,
                        new_serial: Optional[str] = None,
                        new_text: Optional[str] = None) -> Tuple[bool, str]:
    """
    Update an existing scalar entry.
    
    Args:
        level: The scalar level
        old_serial: Current serial of the entry to update
        new_serial: New serial (optional)
        new_text: New text content (optional)
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    collection = get_scalar_collection()
    
    # Find the entry
    entries = collection.get_by_level(level)
    entry = next((e for e in entries if e.serial == old_serial), None)
    
    if entry is None:
        return (False, f"Entry not found: {level.value} {old_serial}")
    
    # Check for duplicate serial if changing
    if new_serial and new_serial != old_serial:
        if any(e.serial == new_serial for e in entries if e.serial != old_serial):
            return (False, f"Serial '{new_serial}' already exists for {level.value}")
    
    # Update fields
    if new_serial:
        entry.serial = new_serial.strip()
    if new_text:
        text = new_text.strip()
        # Validate Bloom's verb for CLOs
        if level == ScalarLevel.CLO:
            has_verb, verb, corrected = check_blooms_verb(text)
            entry.text = corrected
            if not has_verb:
                add_warning(f"Warning: CLO {entry.serial} does not start with a Bloom's performance verb.")
        else:
            entry.text = text
    
    mark_dirty()
    return (True, f"Updated {level.value}: {entry.serial}")


def delete_scalar_entry(level: ScalarLevel, serial: str, 
                        auto_renumber: bool = True) -> Tuple[bool, str]:
    """
    Delete a scalar entry.
    
    Args:
        level: The scalar level
        serial: Serial of the entry to delete
        auto_renumber: If True, renumber remaining entries after deletion
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    collection = get_scalar_collection()
    
    if not collection.remove_entry(level, serial):
        return (False, f"Entry not found: {level.value} {serial}")
    
    if auto_renumber:
        collection.renumber_level(level)
    
    mark_dirty()
    return (True, f"Deleted {level.value}: {serial}")


def reorder_scalar_entries(level: ScalarLevel, serials_in_order: List[str],
                           auto_renumber: bool = True) -> Tuple[bool, str]:
    """
    Reorder entries within a level.
    
    Args:
        level: The scalar level
        serials_in_order: List of serials in the desired order
        auto_renumber: If True, renumber entries based on new order
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    collection = get_scalar_collection()
    
    # Validate that all serials exist
    existing = {e.serial for e in collection.get_by_level(level)}
    for serial in serials_in_order:
        if serial not in existing:
            return (False, f"Serial '{serial}' not found in {level.value}")
    
    collection.reorder_level(level, serials_in_order)
    
    if auto_renumber:
        collection.renumber_level(level)
    
    mark_dirty()
    return (True, f"Reordered {level.value} entries")


def move_entry_up(level: ScalarLevel, serial: str) -> Tuple[bool, str]:
    """Move an entry up one position in its level."""
    collection = get_scalar_collection()
    entries = collection.get_by_level(level)
    serials = [e.serial for e in entries]
    
    idx = serials.index(serial) if serial in serials else -1
    if idx <= 0:
        return (False, "Cannot move up: already at top or not found")
    
    # Swap with previous
    serials[idx], serials[idx - 1] = serials[idx - 1], serials[idx]
    return reorder_scalar_entries(level, serials)


def move_entry_down(level: ScalarLevel, serial: str) -> Tuple[bool, str]:
    """Move an entry down one position in its level."""
    collection = get_scalar_collection()
    entries = collection.get_by_level(level)
    serials = [e.serial for e in entries]
    
    idx = serials.index(serial) if serial in serials else -1
    if idx < 0 or idx >= len(serials) - 1:
        return (False, "Cannot move down: already at bottom or not found")
    
    # Swap with next
    serials[idx], serials[idx + 1] = serials[idx + 1], serials[idx]
    return reorder_scalar_entries(level, serials)


# ============================================================================
# Validation
# ============================================================================

def validate_all_clos(collection: Optional[ScalarCollection] = None) -> List[str]:
    """
    Validate all CLOs for Bloom's verbs.
    
    Args:
        collection: Optional collection to validate (uses session state if None)
        
    Returns:
        List of warning messages for CLOs without Bloom's verbs
    """
    if collection is None:
        collection = get_scalar_collection()
    
    warnings = []
    clos = collection.get_by_level(ScalarLevel.CLO)
    
    for clo in clos:
        has_verb, verb, corrected = check_blooms_verb(clo.text)
        if not has_verb:
            warning = f"Warning: CLO {clo.serial} does not start with a Bloom's performance verb."
            warnings.append(warning)
            add_warning(warning)
        else:
            # Auto-capitalize the verb
            clo.text = corrected
    
    return warnings


def get_blooms_suggestions() -> List[str]:
    """Get a sample of Bloom's verbs for UI suggestions."""
    return sorted(list(BLOOMS_VERBS))[:20]


# ============================================================================
# Save / Load / Clear
# ============================================================================

def save_scalar_to_course(course_scalar: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Get scalar data ready for saving to Course.scalar.
    
    Args:
        course_scalar: The current Course.scalar (will be replaced)
        
    Returns:
        New list of dicts to assign to Course.scalar
    """
    collection = get_scalar_collection()
    mark_clean()
    return collection.to_list()


def load_scalar_from_course(course_scalar: List[Dict[str, Any]]) -> None:
    """
    Load scalar data from Course.scalar into session state.
    
    Args:
        course_scalar: List of dicts from Course.scalar
    """
    collection = ScalarCollection.from_list(course_scalar)
    set_scalar_collection(collection)
    mark_clean()
    validate_all_clos(collection)


def clear_scalar() -> None:
    """Clear all scalar data in session state."""
    st.session_state[SCALAR_STATE_KEY] = ScalarCollection()
    st.session_state[SCALAR_WARNINGS_KEY] = []
    st.session_state[SCALAR_DIRTY_KEY] = True


def clear_level(level: ScalarLevel) -> Tuple[bool, str]:
    """Clear all entries of a specific level."""
    collection = get_scalar_collection()
    count = collection.count_by_level(level)
    collection.clear_level(level)
    mark_dirty()
    return (True, f"Cleared {count} {level.value} entries")


# ============================================================================
# Utility Functions
# ============================================================================

def get_entries_for_display(level: ScalarLevel) -> List[Dict[str, Any]]:
    """
    Get entries formatted for UI display.
    
    Returns:
        List of dicts with 'serial', 'text', 'order_index' keys
    """
    collection = get_scalar_collection()
    entries = collection.get_by_level(level)
    return [
        {
            "serial": e.serial,
            "text": e.text,
            "order_index": e.order_index,
        }
        for e in entries
    ]


def get_level_count(level: ScalarLevel) -> int:
    """Get count of entries for a level."""
    return get_scalar_collection().count_by_level(level)


def get_all_counts() -> Dict[str, int]:
    """Get counts for all levels as a dict with string keys."""
    collection = get_scalar_collection()
    counts = collection.get_counts()
    return {level.value: count for level, count in counts.items()}


def get_next_serial(level: ScalarLevel) -> str:
    """Get the next auto-generated serial for a level."""
    count = get_level_count(level)
    return str(count + 1)

