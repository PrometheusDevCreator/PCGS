# 1. GLOBAL UI CONTRACT — Prometheus V2



File Name: PROMETHEUS_UI_SPEC.md

Placement: Root of repo (PCGS or Prometheus folder — your choice, but Codex will need the instruction below)



## 1.1 Visual Environment

### Background



Global background for all Prometheus screens:



Base: #0A0A0A (solid black)



Overlay: very subtle radial gradient (grey at ~8–10% opacity) centered behind the main workspace panel



No variations per tab — identical environment everywhere



### Canvas Spacing



Outer margin around main content: 32–48px



No element flushes directly against viewport boundaries



Prometheus should always "float" in a dark environment



## 1.2 Colour System (Authoritative Palette)

| Colour Name | Hex | Opacity | Purpose |
|-------------|-----|---------|---------|
| Prometheus Black | #0A0A0A | 100% | Global background |
| Neon Blue | #00E5FF | 70–100% | Primary borders, frames |
| Glow Yellow | #FFD966 | 80% | AI panel borders, highlights |
| Glass Silver Light | #BFC1C6 | 100% | Button gradient top |
| Glass Silver Dark | #8C8E92 | 100% | Button gradient bottom |
| Soft Grey | #C7C7C7 | 100% | Secondary text |
| Inactive Grey | #4E4E4E | 60% | Disabled elements |
| Pure White | #FFFFFF | 100% | Primary text |



All screens enforce these colours.

Codex must not generate new colours unless explicitly added to this table.



## 1.3 Typography



Primary font: Bahnschrift SemiCondensed

Fallback: Bahnschrift → Segoe UI → Arial



### Headings



Size: 18–24px



Weight: SemiBold



Case: UPPERCASE



Colour: White



### Body Text



Size: 14–16px



Weight: Regular



Colour: White or Soft Grey (secondary)



### Buttons



Size: 16–18px



Weight: SemiBold



Colour: White



Case: UPPERCASE



No per-tab variation.



## 1.4 Panel Styling



Applies to all panels across all tabs.



Corner Radius: 24–30px



Stroke: 4px Neon Blue (or Glow Yellow for AI panel)



Outer Glow:



Colour: same as stroke



Blur: 24–32px



Opacity: 20–35%



### Panel Interior



Fill: #0A0A0A (transparent black look)



Very faint inner shadow:



Black at 20% opacity



Blur: 12px



Inset



This creates the "dark glass" Prometheus aesthetic.



## 1.5 Buttons (Primary Action Buttons)

### Shape



Rounded rectangle



Radius: 24px



Height: 50–60px



Width: full container width (unless top bar actions, which use 80–100px)



### Style



Background:



Linear gradient: Glass Silver Light → Glass Silver Dark



Border:



2–3px white stroke



Shadows:



Very light inner shadow to simulate glass



### Hover State



Increase brightness +10%



Strengthen border to 3px



### Pressed State



Inner shadow emphasis



Simulated "press-in"



Buttons must never use Streamlit defaults.



## 1.6 Global Top Bar (Fixed Across All Tabs)



Left: Prometheus glyph + primary screen title

Right: small glass buttons (Load, Save, Delete, Reset)



Height: 60–70px

Full width

Slight neon-blue outline (1–2px)



## 1.7 Global Bottom Strip (Fixed Across All Tabs)



Full-width bar containing:



Owner



Start Date



Status



Progress Bar



Approved for Use (Y/N)



Text: Soft Grey

Accents: Green (#4AFF80) for Approved flag



## 1.8 Prometheus AI Console (Shared Across All Tabs)



Border: Glow Yellow, 4px stroke



Radius: 28–32px



Height: 140–160px



Interior: #000000



Monospace green terminal font for AI output



This is the single shared assistant zone across the platform.



# 2. LAYOUT TEMPLATES

## Template A — Dashboard 3-Column



Used for HOME page (already spec'd earlier).



Columns:



Left (30%) — Learning Objectives



Center (40%) — Course Info + Description + Manager Buttons



Right (30%) — Generate Tools



## Template B — Manager 2-Column



Used for:



Scalar Manager



Content Manager



Lesson Manager



Columns:



Left (30%) → navigation, library, or course tree



Right (70%) → tables, editors, previews, metadata



Everything sits inside a larger main frame using the standard panel styling.



## Template C — Full-Width Workspace



Used for future large-table or full-editor screens.



One single large workspace panel



Top bar + bottom strip remain



Prometheus AI console either bottom-docked or floating on right

