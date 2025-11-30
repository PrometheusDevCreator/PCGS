# Prometheus Course Generation System (PCGS)

Prometheus is a modular, AI-assisted platform for designing, structuring, and generating 
professional-grade courseware. It unifies metadata management, learning outcome development, 
scalar construction, content organisation, lesson building, timetable planning, and 
automated document export (PPTX, DOCX, XLSX).

This repository contains:
- Source code for Prometheus (UI, logic, templates)
- Documentation and development notes
- Export templates and theming resources
- The Promethean Knowledge Engine (PKE) beta logic
- Project-level workflow and governance documents

---

# 1. System Architecture Overview

Prometheus operates under a layered structure:

/prometheus_app
/ui
/logic
/services
/templates
/assets
/utils
/docs
/tests
VERSION
README.md


- **UI Layer**: Tabs, controls, front-end interactions.
- **Logic Layer**: Course framework builder, scalar generator, content parser, PKE hooks.
- **Services**: Export engines (PPTX/DOCX/XLSX), template loaders, validators.
- **Assets/Templates**: PPTX and DOCX templates; themes.
- **Utils**: Helpers, file management, logging.
- **Docs**: Specs, workflow instructions, governance files.

---

# 2. Development Workflow (Operational Doctrine)

Prometheus development follows a two-environment model:

### **A. Architecture & Strategy → Handled in ChatGPT (“Sarah”)**
All:
- System architecture decisions  
- Workflow design  
- PKE behaviour  
- UI redesign approval  
- Template strategy  
- Conceptual alignment  
- Feature requirements  

must be agreed and validated in the **Prometheus project thread**.

### **B. Implementation & Repo Interaction → Handled in Codex (VS Code / Cursor)**
Codex (or the ChatGPT coding environment) is used for:
- File creation
- Code generation
- Repo browsing
- Git commits
- Diffs & merges
- Issue resolution
- Testing automation

Codex references this README plus the Project Instructions and Master Spec during execution.

---

# 3. Command Update Brief (CUB) Protocol

Codex is authorised to produce a **standardised “Command Update Brief” (CUB)**  
whenever the developer issues the prompt:

> **“Generate CUB.”**

The CUB contains:

======================
COMMAND UPDATE BRIEF

REPO STRUCTURE SNAPSHOT

Directories

Key files

Missing/renamed assets

New additions

FILE STATE SUMMARY

Last modified files

New files

Deleted files

Files with unresolved TODOs

Files with implementation drift

VERSION & BRANCH STATUS

Current VERSION file

Active branches

Last merge

Pending merges

Branch conflicts

CODE HEALTH

Syntax errors

Linting issues

Broken imports

Failing tests

Dependency mismatches

WORKSTREAM STATUS

What’s implemented

What’s in-progress

What awaits testing

What requires Sarah’s architectural approval

Risks & flagged inconsistencies

ACTION RECOMMENDATIONS

Required fixes

Merge actions

File clean-ups

Alignment updates


Codex outputs the CUB **as plain text** for easy copy into the ChatGPT/Sarah thread.

---

# 4. Synchronisation Method (Air-Gap Bridge)

Because ChatGPT does not (yet) directly access GitHub repositories:

1. Developer requests a CUB from Codex.  
2. Codex produces structured repo intelligence.  
3. Developer pastes the CUB into the ChatGPT project thread.  
4. Sarah updates architectural understanding and checks for divergence from:
   - Project Instructions
   - Master Spec Sheet
   - Repo state
   - Workflow governance

This loop preserves:
- architectural consistency  
- implementation discipline  
- version integrity  
- strategic oversight  

while staying lightweight and non-duplicative.

---

# 5. Governance Files
- `PROMETHEUS_PROJECT_INSTRUCTIONS.md` — Governing doctrine
- `MASTER_SPEC_SHEET` — Detailed implementation spec
- `README.md` — Public/developer overview
- `README.SUPP.md` — Internal workflow summary (ChatGPT-side coordination)

---

# 6. Licensing / Contacts
TBD




