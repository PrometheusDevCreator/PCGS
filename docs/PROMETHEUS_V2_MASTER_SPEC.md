# PROMETHEUS COURSE GENERATION SYSTEM (PCGS) – V2 MASTER SPECIFICATION

## 1. Background

1. The current Prometheus Course Generation System (PCGS) runs on Streamlit and already supports rapid generation of training course documentation (lesson plans, timetables, PowerPoints, etc.).
2. Course design currently starts with manual entry of basic course settings (name, code, duration, thematic area, skill level, developer name), followed by further data entry/import to complete the course.
3. The existing system has grown iteratively. As a result:
   - The codebase contains inefficiencies and redundant sections.
   - Some functionality is unreliable or broken.
   - The UI, while functional, needs improvement in appearance and workflow to match a premium, professional product.
4. Live testing has confirmed the need for a ground-up redesign that is robust, modular, testable, and visually modern.

---

## 2. Overall Intent

1. Perform a **ground-up redesign** of PCGS using good practice in structure and modularisation.
2. Deliver an **upgraded UI** that:
   - Looks premium, sharp, crisp, and professional.
   - Guides users through the workflow clearly and logically.
3. Ensure **full, reliable functionality**, including:
   - Stable imports and exports in all required formats.
   - Space for new features (e.g. agents, advanced exports).
4. Design the system so it can be:
   - Deployed reliably (e.g. Railway or similar).
   - Extended later with a richer web front-end (e.g. React) and design tooling (e.g. Figma), without major rewrites.

---

## 3. User & Development Workflow

### 3.1 Matthew’s Working Setup

1. Primary development interface: **Cursor** on desktop.
2. Matthew does **not write code directly**. All instructions and feedback are provided via plain text.
3. Active AI subscriptions: ChatGPT Plus, Claude, Gemini (these may be used behind the scenes via Cursor or other tools).
4. Version control: **GitHub** repository already linked to Cursor.
5. Hosting: **Railway** account available for deployment.

### 3.2 Development Agent Expectations

1. The coding agent/system must:
   - Read and understand Matthew’s written requirements.
   - Summarise instructions back to him before making changes.
   - Ask clarification questions where needed.
   - Propose a plan, then implement it.
2. All significant changes should:
   - Be committed to Git with clear messages.
   - Go through a branch/PR workflow where possible.
   - Be merged to `main` only with Matthew’s explicit approval.

---

## 4. High-Level System Goals

1. **PCGS Core Engine** – A clean, modular Python package that handles course structures, scalars, lessons, timetables, and exports.
2. **UI Layer** – Initially Streamlit, but designed so:
   - The UI is separate from the core logic.
   - A future React web front-end (designed in Figma if desired) can be added later by talking to the core via a simple API.
3. **PKE (Promethean Knowledge Engine)** – An AI agent layer, initially with placeholder functions and clear interfaces, so full AI features can be implemented as a separate body of work.
4. **Export Layer** – Reliable exports:
   - PowerPoint (PPTX)
   - Word documents (DOCX)
   - Excel or CSV where needed
   - Course summary / proposal documents
5. **Security & Stability** – User management, safe handling of data, versioned changes, and tests.

---

## 5. System Architecture

### 5.1 Layered Design

PCGS v2 must be structured into clear layers:

1. **Core Engine (pcgs_core)**
   - Pure Python logic.
   - Knows nothing about UI frameworks.
   - Handles course data models, validation, workflows, and export hooks.

2. **Agent Layer (pcgs_agents / PKE)**
   - Provides a clean interface for AI-powered actions (e.g. generate CLOs, write course descriptions).
   - Initially implemented as placeholders with mock responses and clear function signatures.
   - Later can be wired to real LLM calls (ChatGPT, Claude, Gemini).

3. **UI Layer**
   - **Phase 1**: Streamlit app (`pcgs_ui_streamlit` or `app.py` calling UI functions).
   - **Phase 3+**: Optional React front-end that communicates with an API (e.g. FastAPI backend wrapping `pcgs_core`).
   - All UI events (buttons, forms, etc.) must call into `pcgs_core` or the Agent Layer rather than containing business logic directly.

4. **Storage Layer**
   - Start with local storage (JSON, SQLite, or simple files) for user data and course content.
   - Design data access via a clear interface so that a database (e.g. Postgres) can be plugged in later with minimal changes.

5. **Export Layer**
   - Functions to convert internal data structures into PPTX, DOCX, and other formats using templates.
   - Separated into a dedicated module (e.g. `pcgs_exports`) so that templates or export formats can be updated or replaced.

---

## 6. Data Model Overview

The following are conceptual models (exact implementation can use Pydantic or dataclasses).

### 6.1 Core Entities

- **User**
  - `id`
  - `name`
  - `email`
  - `role` (Admin / User)
  - `password_hash`
  - `created_at`

- **Course**
  - `id`
  - `name`
  - `code`
  - `duration_days`
  - `thematic_area`
  - `level`
  - `description`
  - `developer` (linked to User)
  - `scalar` (list of course objectives/structure items)
  - `lessons` (list of Lesson objects)
  - `timetable` (structured schedule)
  - `metadata` (e.g. language, brand, tags)
  - `created_at`, `updated_at`

- **Lesson**
  - `id`
  - `course_id`
  - `title`
  - `linked_scalar_items`
  - `duration_blocks`
  - `content_sections` (key teaching points, activities, notes)
  - `resources`
  - `assessment_items` (if any)

- **Timetable**
  - Represents days, time blocks, and which lessons/activities appear where.
  - Must reflect Rabdan standard day structure but allow manual overrides.

These models must be defined clearly in `pcgs_core.models` (or equivalent) and used consistently across UI, exports, and agents.

---

## 7. Security & User Management

1. **Login & Roles**
   - User login with Admin/User roles.
   - Admin can manage users and settings.
   - Regular users can create and manage their own courses.

2. **Registration**
   - On first use, users create a username, email, and password.
   - This data must persist across code updates (stored in a stable location, not erased on deploy).

3. **Forgotten Password**
   - Function where users enter their registered email.
   - System sends a reset link or one-time code (implementation detail can be simplified but must follow a secure, sensible pattern).

4. **Security Practices**
   - Passwords stored using strong hashing (e.g. bcrypt).
   - API keys or secrets (for PKE) stored via environment variables, not hard-coded.
   - Basic logging of key actions (logins, course creation, exports, errors).

---

## 8. UI Strategy

### 8.1 Immediate UI (Streamlit)

1. Use Streamlit for the initial version to get a functional, professional UI online quickly.
2. Requirements:
   - Consistent layout with a left-side navigation or top-navigation bar.
   - Clean typography (clear, legible font choices).
   - A neutral, modern colour palette matching a premium professional tool (with room to add brand themes like Rabdan later).
   - Clear separation across pages/tabs:
     - Login / Registration
     - Dashboard (existing courses, new course)
     - Course Setup
     - Scalar Builder
     - Lesson Builder
     - Timetable Builder
     - Export Centre
     - Settings (user profile, theme, language, etc.)

3. The UI should guide the user step-by-step, but still allow jumping back to earlier steps to edit information.

### 8.2 Future UI (React + Figma Ready)

1. The system should be designed so that:
   - A future React front-end can be built to replace or sit alongside Streamlit.
   - Figma can be used to design screen layouts, components, and flows.
2. To support this:
   - UI logic and page structure should be described in a way that a designer or front-end dev can understand easily.
   - `pcgs_core` functions must be callable via a simple API (e.g. FastAPI or similar) at a later phase.
   - Naming, components, and flows should be documented in Markdown so they can be mirrored in Figma.

---

## 9. PKE (Promethean Knowledge Engine) – Placeholder Design

1. PKE is the AI layer; it will eventually:
   - Generate course descriptions.
   - Propose CLOs / scalars.
   - Draft lesson content and activities.
   - Suggest assessments and handbooks.

2. For v2 initial implementation:
   - Provide **placeholder functions** with clearly defined signatures:
     - `generate_course_description(input: CourseBrief) -> str`
     - `generate_scalar(input: CourseBrief) -> List[ScalarItem]`
     - `generate_lessons(input: Course + Scalar) -> List[Lesson]`
   - These functions may return simple stub data or call a local mock generator.
   - All PKE calls should be routed through a single module or class (`pcgs_agents.pke`), making the later integration of real APIs straightforward.

3. When eventually integrated with real LLMs:
   - The PKE must return structured JSON-compatible data, not just free text.
   - Errors and uncertainties must be clearly reported back to the user rather than silently failing.

---

## 10. Export & Template System

1. All exports (PPTX, DOCX, etc.) must:
   - Use template files stored in a dedicated `templates/` folder.
   - Separate data from presentation (content from formatting).

2. Requirements:
   - Support at least:
     - Course PPT
     - Lesson Plans (DOCX or PDF)
     - Timetable
     - Course Summary / Proposal (DOCX)
     - Learner/Student Handbook (later phase)
     - Assessments and QA forms (later phase)

3. Template handling:
   - Allow multiple template “profiles” (e.g. Rabdan, generic).
   - Make it easy to add or switch templates without changing core code.
   - Clearly document placeholder fields and how they map to course data.

---

## 11. Testing & Quality

1. **Unit Tests**
   - For all core engine functions (models, scalar generation logic, timetable logic, export data preparation, etc.).

2. **Integration Tests**
   - End-to-end checks for:
     - Creating a course.
     - Building a scalar.
     - Building lessons.
     - Creating a timetable.
     - Exporting a PPTX and DOCX.

3. **UI Smoke Tests**
   - Basic checks that main pages render without errors and that primary buttons/forms work.

4. **Pre-Delivery Expectations**
   - New features should be accompanied by relevant tests.
   - Tests must pass before code is considered “ready” for Matthew to review.

---

## 12. Versioning & Change Management

1. Use **semantic versioning**:
   - `MAJOR.MINOR.PATCH` (e.g. 2.0.0, 2.1.0).
2. Keep a `CHANGELOG.md` summarising:
   - New features.
   - Fixes.
   - Breaking changes.
3. Development workflow:
   - Use feature branches (e.g. `feature/ui-dashboard`, `feature/export-system`).
   - Use pull requests for non-trivial changes.
   - Matthew approves merges into `main`.

---

## 13. PCGS User Workflow (Functional Flow)

1. **User Logon & Registration**
   - New users register with name, email, password.
   - Returning users log in.
   - Roles: Admin / User.

2. **Load or Create Course**
   - Existing course list with search/filter.
   - “Create New Course” wizard.

3. **Course Creation – Required Inputs**
   - Course Name
   - Course Level
   - Course Thematic Area
   - Duration (Days)
   - Course Code
   - Developer Name auto-populated from logged-in user.

4. **Optional Description (Manual + PKE)**
   - User may:
     - Type a description.
     - Paste a description.
     - Ask PKE to generate one based on brief inputs.

5. **Scalar Creation**
   - Manually input scalar (learning objectives, topics, structure).
   - Import from Excel.
   - Ask PKE to propose a scalar.
   - Optionally create a Course Technical Proposal / Summary (DOCX) at this stage.

6. **Content Gathering & Organisation**
   - Manual input (text, bullet points, notes).
   - Import from existing documents (where possible).
   - Ask PKE to generate or augment content.

7. **Lesson Building**
   - Build lessons based on scalar + content.
   - User can add/edit content at any time.
   - Optionally ask PKE to auto-construct lessons.

8. **Timetable Definition**
   - Manual timetable designer (drag/drop or structured form).
   - Optionally auto-generate timetable based on duration and lesson lengths.
   - Respect Rabdan-style teaching day structure but allow overrides.

9. **Exports**
   - Export:
     - Timetable
     - Lesson Plans
     - Course PPT
     - Course/Technical Proposal
     - Later: Learner Handbook, Assessments, QA forms.
   - Allow manual tweaks before final export where appropriate.

10. **Editing & Iteration**
    - User can manually edit any data element.
    - Changes propagate correctly across views and exports.

---

## 14. Non-Negotiables

These must never be compromised:

1. **Reliability of Exports** – Documents must open cleanly and use correct templates.
2. **Stability of User Data** – No silent loss of data. Changes and saves must be predictable and safe.
3. **Modularity of Architecture** – Core engine, UI, agents, and exports remain cleanly separated.
4. **Transparency of AI Outputs** – Users always know when PKE has been used, and can see/edit its outputs.
5. **User Control** – Users can override and manually edit anything the system or agents produce.
6. **No Hidden Changes** – No UI or functionality changes without Matthew’s express permission.
7. **Auditability** – Basic logging exists for debugging and review of system behaviour.

---

## 15. Constraints & Behaviour Expectations

1. **Do not second-guess requirements.**
   - Follow written instructions; ask for clarification when unsure.

2. **Never alter UI or functionality without explicit permission.**
   - Cosmetic and workflow changes must be discussed and agreed first.

3. **Analyse instructions and summarise before acting.**
   - For each significant task:
     - Read Matthew’s instructions.
     - Summarise them briefly to confirm understanding.
     - Only then proceed.

4. **Language & Communication**
   - Avoid technical jargon where it’s not essential.
   - Use clear, straightforward explanations.
   - Keep responses concise but precise.

5. **Self-Critique**
   - Consider alternative approaches.
   - If there is a better way of doing something, propose it and explain why.

---

## 16. Project Phases

**Phase 1 – Foundations**
- Set up repository structure.
- Implement `pcgs_core` skeleton (models, basic workflows).
- Implement simple Streamlit UI skeleton.
- Add basic tests and CI checks.

**Phase 2 – Core Engine**
- Implement full data models (Course, Lesson, Timetable, etc.).
- Implement scalar, lesson, and timetable logic.
- Add storage layer (file/SQLite).

**Phase 3 – UI Build & UX**
- Build all main Streamlit pages and flows.
- Apply premium, clean visual styling.
- Ensure navigation is intuitive and minimal clicks.

**Phase 4 – Export System**
- Implement PPTX and DOCX exports using templates.
- Implement course summary/proposal export.
- Test exports thoroughly.

**Phase 5 – PKE Integration (Placeholder to Real)**
- Implement placeholder PKE functions with solid interfaces.
- Later: connect to real LLM APIs with environment-based configuration.

**Phase 6 – Security & User Management**
- Implement login, registration, roles, password handling.
- Implement “forgotten password” flow.
- Add logging.

**Phase 7 – Deployment & Optimisation**
- Set up Railway (or similar) deployment.
- Optimise performance.
- Hardening, bug fixes, documentation updates.

---

## 17. Documentation

1. Maintain a `/docs` folder containing:
   - This master specification.
   - Architecture diagrams (simple, text-based if needed).
   - UI flow descriptions.
   - Template mapping (content → placeholders).
   - PKE interface descriptions.

2. Ensure documentation is kept up to date as features evolve.

---

_End of PROMETHEUS V2 Master Specification._
