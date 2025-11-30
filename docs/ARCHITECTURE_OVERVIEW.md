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
    *   The legacy user interface (V1).
    *   Initially built with Streamlit.
    *   Communicates with `pcgs_core` to perform actions.
    *   Contains **no** business logic; only view logic.
    *   **Being superseded by pcgs_app for V2.**

5.  **Application Layer (`pcgs_app`)** *(NEW in V2)*:
    *   The new Prometheus V2 application module.
    *   Provides a clean separation between core logic, services, and UI.
    *   Structure:
        *   `core/` - Models and storage facades
        *   `logic/` - Business logic and lexicon definitions
        *   `services/` - Service layer (scalar management, importers)
        *   `ui/` - Streamlit UI components organized by feature

## 2. Directory Layout

```
root/
├── docs/                   # Project documentation and specs
├── src/
│   ├── pcgs_core/          # Domain logic, models, workflows
│   ├── pcgs_agents/        # AI/PKE integration
│   ├── pcgs_exports/       # Export logic (PPTX, DOCX)
│   ├── pcgs_ui_streamlit/  # Legacy Streamlit application (V1)
│   └── pcgs_app/           # NEW: Prometheus V2 Application
│       ├── core/           # Models, storage facades
│       │   ├── models.py
│       │   ├── storage.py
│       │   └── scalar_models.py  # Scalar data models
│       ├── logic/          # Business logic
│       │   └── lexicon.py  # Canonical terminology (Lex enum)
│       ├── services/       # Service layer
│       │   ├── scalar_service.py  # Scalar CRUD + validation
│       │   └── importer/   # Import logic
│       └── ui/             # UI components
│           ├── tabs/       # Tab renderers
│           │   ├── tab_create_course.py  # Dashboard
│           │   └── tab_scalar.py         # Scalar Manager V2
│           ├── theme/      # Styling and tokens
│           └── widgets/    # Reusable components
├── templates/              # Document templates (for exports)
├── tests/                  # Unit and integration tests
├── app.py                  # Application entry point (launcher)
└── requirements.txt        # Python dependencies
```

## 3. Key Design Principles

*   **Separation of Concerns**: The UI does not know about database implementation details. The Core does not know about Streamlit widgets.
*   **Interface-First**: Agents and Storage are defined by interfaces, allowing implementations to change (e.g., from local JSON to SQL, or from Mock AI to Real AI) without breaking the system.
*   **Template-Driven**: Exports rely on external templates, making branding changes easy.
*   **Lexicon-Driven** *(V2)*: All terminology uses canonical `Lex` enum IDs for consistency across UI, storage, and exports.

## 4. Scalar Manager V2

The Scalar Manager is a core component for building course content hierarchy.

### Data Model

The scalar represents the course structure with five levels:
1. **CLO** - Course Learning Objectives (validated against Bloom's Taxonomy)
2. **Topic** - Major course topics
3. **Subtopic** - Sub-divisions of topics
4. **Lesson** - Individual lesson units
5. **Performance Criteria** - Measurable outcomes

```python
# Located in: src/pcgs_app/core/scalar_models.py
class ScalarEntry:
    level: ScalarLevel      # CLO, Topic, Subtopic, Lesson, PerformanceCriteria
    serial: str             # Identifier (e.g., "1", "1.1", "1.1.1")
    text: str               # Content text
    order_index: int        # UI ordering
    parent_serial: str      # Optional parent reference
    metadata: Dict          # Additional data (Bloom's status, etc.)
```

### Service Layer

All scalar operations go through `scalar_service.py`:
- `import_scalar_from_excel(file)` - Import from Excel template
- `add_scalar_entry(level, serial, text)` - Add new entry
- `update_scalar_entry(level, serial, ...)` - Update existing entry
- `delete_scalar_entry(level, serial)` - Remove entry
- `reorder_scalar_entries(level, serials)` - Change order
- `validate_all_clos()` - Check Bloom's verbs

### Excel Import Contract

The Excel template follows this structure:
- **Row 6+**: Data rows
- **Columns B/C**: CLO serial + text
- **Columns D/E**: Topic serial + text
- **Columns F/G**: Subtopic serial + text
- **Columns H/I**: Lesson serial + text
- **Columns J/K**: Performance Criteria serial + text

### Bloom's Taxonomy Validation

CLO entries are automatically validated for Bloom's verbs:
- Verbs are checked case-insensitively against a curated list
- First word is auto-capitalized if it's a valid Bloom's verb
- Warnings are displayed (but don't block saving) for invalid CLOs

## 5. Navigation Flow

The V2 application follows this navigation pattern:

```
Dashboard (Create Course)
    │
    ├── Course Info Panel
    ├── Course Description Panel  
    ├── Learning Objectives Panel
    │
    └── Manager Tiles ─────────────────┐
                                       │
        ┌──────────────────────────────┘
        ▼
    Scalar Manager ──────► Content Manager ──────► Lesson Manager
        │                      (TODO)                 (TODO)
        │
        └── RETURN TO FRONT PAGE (back to Dashboard)
```

Navigation is managed via Streamlit session state:
- `pcgs_navigate_to_tab` - Set by manager buttons to request tab switch
- `pcgs_current_tab` - Current active tab ID
- Sidebar radio controls tab selection in main app shell







