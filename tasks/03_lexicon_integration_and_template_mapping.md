
---

## STEP 3 – Draft for `tasks/03_lexicon_integration_and_template_mapping.md`

Create:  
`tasks/03_lexicon_integration_and_template_mapping.md` with:

```markdown
# Task 03 – Lexicon Integration & Template Mapping

## Objective

Adopt the **Prometheus Lexicon** as the single source of truth for field
names and map it into exporters and templates so v2 is **institution-agnostic**
and template-driven.

## Scope

This task covers:

- Integrating `pcgs_app.logic.lexicon` (Lex enum + helpers) into:
  - Models
  - Workflows
  - UI tab definitions
  - Exporters (PPTX/DOCX/XLSX)
- Creating template map structures that connect **Lex IDs** to:
  - Placeholder names inside PPTX / DOCX templates
  - Row/column definitions in timetable and lesson-plan spreadsheets
- Cleaning up legacy string constants for fields (e.g. `"course_name"`)
  and replacing them with Lex IDs.

---

## Work Items

### 1. Wire Lex into Models & Workflows

- Update `pcgs_core.models` and any new `pcgs_app.core` models so that
  course structures use Lex IDs for keys where possible:

  ```python
  from pcgs_app.logic.lexicon import Lex

  course_payload = {
      Lex.C_NAME.value: "...",
      Lex.C_LEVEL.value: "...",
      Lex.C_THEME.value: "...",
      Lex.C_DURATION.value: 3,
      Lex.C_DEV.value: "...",
      Lex.C_DESC.value: "...",
  }

Ensure workflow functions in pcgs_core.workflows and
pcgs_app.logic.workflows accept and return data that can be keyed by
Lex IDs (even if an adapter converts to friendlier shapes for the UI).

2. Centralise Field Names for UI Panels

For each major panel/tab (Create Course, Scalar Manager, Content Manager,
Lesson Manager), define a small mapping from Lex IDs to user-facing labels
near the UI code, e.g.:

FIELD_LABELS = {
    Lex.C_NAME: "Course Title",
    Lex.C_LEVEL: "Level",
    Lex.C_THEME: "Thematic",
}


Use these dictionaries in the UI instead of hard-coded labels to support
later localisation.

3. Define Template Map Structures

Create a new module src/pcgs_app/services/exporter/template_maps.py
(or similar) that defines template maps such as:

from pcgs_app.logic.lexicon import Lex

RABDAN_PPTX_MAP = {
    Lex.C_NAME: "C_Name",
    Lex.C_LEVEL: "C_Level",
    Lex.C_DESC: "C_Description",
    Lex.SL_TITLE: "SLIDE_TITLE",
    Lex.SL_BODY: "SLIDE_BODY",
    # ...
}


Provide at least one initial map:

DEFAULT_PPTX_MAP (generic)

RABDAN_PPTX_MAP (Rabdan-style, even if not yet used)

Document how exporters retrieve an appropriate map (e.g. via config or
a simple selector in pcgs_exports.templates).

4. Update Exporters to Use Lex IDs

In the PPTX, lesson-plan Excel, and timetable Excel exporters, replace
direct placeholder strings with lookups via the template map:

placeholder = pptx_map[Lex.C_NAME]
_replace_text_in_slide(slide, {placeholder: course[Lex.C_NAME.value]})


Ensure all slide/body fields use Lex.SL_* IDs rather than ad hoc tokens.

5. Provide Normalisation Helpers for Legacy Data

Where the system needs to ingest legacy Prometheus1 JSON or Scalar files,
create small adapters that:

Read legacy keys / column headings.

Use normalise_term() to resolve them to Lex IDs.

Emit a standardised structure keyed by Lex IDs.

Acceptance Criteria

lexicon.py compiled and imported without errors; Lex enum used in:

At least one model

At least one workflow

The Create Course tab

At least one PPTX template map defined using Lex keys.

At least one exporter (PPTX or Excel) updated to:

Use template maps

Access data via Lex IDs

No remaining “mystery” string constants for core course fields
(course_name, course_level, etc.) in the updated modules.

A short usage note is added to docs/LEXICON_REFERENCE.md if behaviour
changes.

Notes

This task does not require full migration of all v1 logic; it only
ensures that any new v2 code is lexicon-aware.

Additional Lex IDs may be added as needed; when they are, both
lexicon.py and LEXICON_REFERENCE.md must be updated together.