# PCGS v2 Architecture Overview

## 1. High-Level Structure

PCGS v2 follows a modular, layered architecture designed for scalability, testability, and future expansion.

### Layers

1.  **PCGS Core (`pcgs_core`)**:
    *   The heart of the application.
    *   Contains pure Python logic, data models, and business rules.
    *   Independent of any UI or external framework.

2.  **Agent Layer (`pcgs_agents`)**:
    *   Handles AI interactions (PKE - Promethean Knowledge Engine).
    *   Provides clear interfaces for generating content (descriptions, scalars, lessons).
    *   Currently implemented as placeholders; will connect to LLMs in future phases.

3.  **Export Layer (`pcgs_exports`)**:
    *   Manages the conversion of internal data models to external formats (PPTX, DOCX).
    *   Uses templates to separate content from presentation.

4.  **UI Layer (`pcgs_ui_streamlit`)**:
    *   The user interface.
    *   Initially built with Streamlit.
    *   Communicates with `pcgs_core` to perform actions.
    *   Contains **no** business logic; only view logic.

## 2. Directory Layout

```
root/
├── docs/                   # Project documentation and specs
├── src/
│   ├── pcgs_core/          # Domain logic, models, workflows
│   ├── pcgs_agents/        # AI/PKE integration
│   ├── pcgs_exports/       # Export logic (PPTX, DOCX)
│   └── pcgs_ui_streamlit/  # Streamlit application code
├── templates/              # Document templates (for exports)
├── tests/                  # Unit and integration tests
├── app.py                  # Application entry point (launcher)
└── requirements.txt        # Python dependencies
```

## 3. Key Design Principles

*   **Separation of Concerns**: The UI does not know about database implementation details. The Core does not know about Streamlit widgets.
*   **Interface-First**: Agents and Storage are defined by interfaces, allowing implementations to change (e.g., from local JSON to SQL, or from Mock AI to Real AI) without breaking the system.
*   **Template-Driven**: Exports rely on external templates, making branding changes easy.







