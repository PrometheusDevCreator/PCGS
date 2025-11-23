# Prometheus Course Generation System (PCGS) v2

PCGS v2 is a modular, AI-enhanced system for designing training courses and generating documentation (Lesson Plans, Timetables, PPTX).

## Project Structure

See `docs/ARCHITECTURE_OVERVIEW.md` for a detailed breakdown.

- `src/pcgs_core`: Domain logic and models.
- `src/pcgs_agents`: AI/PKE integration.
- `src/pcgs_ui_streamlit`: User Interface.
- `src/pcgs_exports`: Document generation.

## Getting Started

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  Run the application:
    ```bash
    streamlit run app.py
    ```
    OR
    ```bash
    python app.py
    ```

3.  Run tests:
    ```bash
    pytest
    ```

## Status

**Phase 1 (Foundations)**: Initial skeleton and architecture setup complete.
