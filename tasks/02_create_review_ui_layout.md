# Task 02 – Create Course Sci-Fi UI Layout (Tab 1)

## Objective

Design and implement the **Prometheus v2** “Create Course” / “Course Hub”
screen using the neon sci-fi layout, with PKE integration and state-driven
visual feedback. This becomes the **primary entry point** for course setup.

## Scope

This task covers:

- The **visual layout** of Tab 1:
  - Course Information reactor-core (centre top)
  - Course Description panel
  - Learning Objectives panel
  - Scalar / Content / Lesson Manager node row
  - PKE terminal band
  - Generate panel (right-hand exports column)
  - Status strip (bottom: owner, start date, status, progress, approval)
- **State rules** for:
  - “Complete”, “Unsaved changes”, and “PKE active”
  - Connector glow and node icon states
- **PKE placeholder behaviour** for:
  - Course Description
  - Course Learning Objectives
- Wiring the tab into `pcgs_app.ui.tabs.tab_create_course` using the theme
  tokens and Streamlit CSS.

Backend logic (saving, exports, PKE real calls) is **out of scope** here and
handled by later tasks.

---

## Functional Requirements

### 1. Course Information Reactor (C_INFO)

- Displays editable fields:
  - Title (Lex.C_NAME)
  - Level (Lex.C_LEVEL)
  - Thematic (Lex.C_THEME)
  - Duration (Lex.C_DURATION)
  - Course Code (Lex.C_CODE, optional)
  - Developer (Lex.C_DEV – auto-fill from user profile but editable)
- Canonical “course info cluster” on the left is **read-only** and mirrors
  saved state (course loaded, duration, level, thematic).
- When any field differs from saved state, the Course Information panel:
  - Enters **“unsaved”** state (soft pulsing edge).
  - Lights the connector to the Save button.

### 2. Course Description Panel (C_DESC)

- Central panel directly under Course Information.
- Multi-line text area representing the **current description**.
- Flame icon inside header triggers PKE:
  - PKE terminal beams in gold.
  - Prompt: _“Would you like me to describe the course?”_
  - User response is entered in the PKE terminal.
  - On “yes”, PKE placeholder writes:
    - Generated description → Course Description panel (C_DESC).
    - PKE commentary remains in the terminal.
  - Panel border glows gold during PKE activity, then soft-pulses until
    user either edits or saves.

### 3. Learning Objectives Panel (CLO)

- Left-hand vertical panel, showing up to **3 CLOs** at a time:
  - Additional CLOs accessible via scroll bar.
  - Each row has a **+** control to add a new objective.
- Panel header includes a flame icon:
  - PKE prompt: _“Would you like me to generate Course Learning Objectives?”_
  - PKE terminal interaction as above.
  - Placeholder logic:
    - Generate CLO 1 → populate first empty slot.
    - Confirm with user; on approval, proceed with CLO 2, etc.
- Once minimum CLO count is met and saved, connector **(2)** to the node row
  glows to indicate Scalar / Content / Lesson Manager are now meaningful.

### 4. Node Row – Scalar, Content, Lesson Managers

- Three square nodes:
  - Scalar Manager (Lex.SCALEMGR)
  - Content Manager (Lex.CONTMGR)
  - Lesson Manager (Lex.LSNMGR)
- Clicking a node switches to the corresponding tab in the application.
- Node appearance:
  - **Dormant**: dim border, icon only.
  - **Available**: steady glow when prerequisites are met.
  - **Active** (current tab): strong glow + small motion (e.g. pulsing icon).
- Timetable logic is conceptually part of Lesson Manager; no separate node.

### 5. PKE Terminal Band

- Gold band along the bottom of the main hub.
- Only shows when any flame icon is pressed.
- Behaviour:
  - Displays PKE question at the top of the band.
  - Shows blinking arrow / cursor for user response.
  - Logs short “action narration” from the PKE (e.g. “Generating CLO 1…”).
- Direct text from PKE is always mirrored into the relevant panel
  (Description, CLOs, etc.), **not** stored solely in the terminal.

### 6. Generate Panel (Exports)

- Right-hand column titled **GENERATE**.
- Contains four buttons (placeholders for now):
  - Course Presentation
  - Handbook
  - Assessments
  - Supporting Materials
- All export buttons are **disabled** until minimum data state is met
  (C_INFO, C_DESC, CLOs). Exact rules handled in a later export task.

### 7. Status Strip

- Bottom strip shows:
  - Owner: (C_DEV)
  - Start date
  - Status (e.g. “IN DEVELOPMENT”)
  - Progress bar percentage
  - Approved for use Y/N
- Initially: progress is a **simple function** of required fields completed
  on this tab (later tasks may refine).

---

## Technical Requirements

- Implement UI in `src/pcgs_app/ui/tabs/tab_create_course.py`.
- Apply theme via:

  ```python
  from pcgs_app.ui.theme.tokens import get_default_tokens
  from pcgs_app.ui.theme.streamlit_theme import apply_base_theme

Use Lex IDs from pcgs_app.logic.lexicon for:

Internal field names

Connector metadata

PKE target fields (C_DESC, CLO)

Use Streamlit layout primitives (st.columns, st.container, etc.) and
CSS classes provided by streamlit_theme.py for styling.

Acceptance Criteria

Tab renders without errors and matches the mock-up intent:

Reactor core layout for Course Information.

Description and CLO panels with flame icons.

Node row and PKE terminal.

Generate panel and status strip.

PKE buttons perform placeholder behaviour:

Interactions happen in the gold terminal band.

Text is written to the appropriate panel.

Panel and connector states update according to:

Unsaved changes (soft pulse).

PKE activity (gold glow).

Completed segments (steady glow).

All internal references to fields on this tab use Lex IDs (no “random”
string constants).