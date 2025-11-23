# Task 01 – Initial Project Structure for PCGS v2

## 1. Context

This task is the **first build step** for the Prometheus Course Generation System (PCGS) v2.

You **must** follow the definitions and intent in:

- `docs/PROMETHEUS_V2_MASTER_SPEC.md`

Do **not** invent your own architecture or workflow. Use that document as the single source of truth.

Before doing anything, **read and summarise** the master spec so the user can confirm your understanding.

---

## 2. Goal

Set up a clean, modular **initial project skeleton** for PCGS v2 that:

1. Matches the layered architecture described in the master spec.
2. Uses a proper Python package structure.
3. Provides a minimal but working Streamlit UI skeleton.
4. Prepares for future addition of:
   - PKE (Promethean Knowledge Engine) agent logic.
   - Export system.
   - React/Figma front-end and API layer.
5. Includes basic testing and documentation scaffolding.

This task is about **structure and foundations**, not full functionality.

---

## 3. Requirements

### 3.1 Repository Layout

In the repo root (the folder containing `.git`), create a structure like this (adjust only if absolutely necessary and explain any deviation):

- `docs/`
  - `PROMETHEUS_V2_MASTER_SPEC.md` (already exists)
  - `ARCHITECTURE_OVERVIEW.md` (new – see below)
- `src/`
  - `pcgs_core/`
    - `__init__.py`
    - `models.py`
    - `config.py`
    - `storage.py`
    - `workflows.py`
  - `pcgs_agents/`
    - `__init__.py`
    - `pke.py`             (placeholder for Promethean Knowledge Engine)
  - `pcgs_exports/`
    - `__init__.py`
    - `templates.py`       (placeholder for template handling)
  - `pcgs_ui_streamlit/`
    - `__init__.py`
    - `main.py`            (Streamlit entrypoint)
- `templates/`
  - `README.md`            (placeholder – explains purpose of this folder)
- `tests/`
  - `test_basic_structure.py`
- `app.py`                 (optional thin launcher, see below)
- `requirements.txt`
- `pyproject.toml` or `setup.cfg` (if appropriate for packaging – can be placeholder)
- `.gitignore`
- `README.md` (top-level project README)

> If some of these files already exist, refactor them into this structure rather than duplicating.

---

### 3.2 Core Engine Skeleton (`pcgs_core`)

Create the following **placeholders with docstrings**, not full implementations:

- `pcgs_core/__init__.py`
  - Expose high-level entry points or version info (can be minimal for now).

- `pcgs_core/models.py`
  - Define minimal placeholder data models for:
    - `User`
    - `Course`
    - `Lesson`
    - `Timetable`
  - Use either `dataclasses` or `pydantic` models.
  - Only include key fields (id, name, code, etc.) – no complex logic yet.
  - Add docstrings linking each model back to the relevant section in the master spec.

- `pcgs_core/config.py`
  - Provide a simple configuration object or function that:
    - Reads environment variables (e.g. for future DB URL, API keys).
    - Contains placeholder defaults.
  - No secrets hard-coded.

- `pcgs_core/storage.py`
  - Define clear **interfaces only** for now, e.g.:
    - `save_course(course: Course) -> None`
    - `load_course(course_id: str) -> Course | None`
    - `list_courses(user_id: str) -> list[Course]`
  - Implement them as simple placeholders that raise `NotImplementedError` or use in-memory storage with clear TODO comments.

- `pcgs_core/workflows.py`
  - Define placeholder functions representing high-level workflows:
    - `create_new_course()`
    - `build_scalar_for_course(course: Course)`
    - `build_lessons_for_course(course: Course)`
    - `build_timetable_for_course(course: Course)`
  - For now, these can just log/print what they would do, with TODO comments.

---

### 3.3 Agent Layer Skeleton (`pcgs_agents`)

Create `pcgs_agents/pke.py`:

- Define placeholder interfaces for the PKE:

  ```python
  def generate_course_description(brief: dict) -> str:
      """Generate a course description based on a brief. Placeholder implementation."""
      ...

  def generate_scalar(brief: dict) -> list[dict]:
      """Generate a scalar structure (CLOs, topics, etc.). Placeholder implementation."""
      ...

  def generate_lessons(course_data: dict) -> list[dict]:
      """Generate lesson outlines based on course and scalar data. Placeholder implementation."""
      ...
