"""
Prometheus Lexicon v1.0.0
==================

Single source of truth for Prometheus terminology and IDs.

This module exposes:

- Lex: Enum of canonical Lexicon IDs (C_INFO, CLO, SCALEMGR, etc.).
- LexiconEntry: dataclass describing each term.
- LEXICON: mapping of Lex -> LexiconEntry.
- normalise_term(): map any user-facing label to a canonical Lex ID.
- get_entry(): retrieve LexiconEntry by ID or variant term.
- is_term(): convenience predicate for comparisons.

Golden rule:
------------
All internal logic, models, template maps, and exporters should refer to
fields using Lex IDs (Lex.C_NAME, Lex.CLO, etc.), *never* raw strings.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


# --------------------------------------------------------------------------- #
# Core structures
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class LexiconEntry:
    """Metadata for a single lexicon item."""

    id: str
    primary_term: str
    variants: List[str]
    category: str
    notes: str = ""


class Lex(str, Enum):
    """Canonical Lexicon IDs.

    Use Lex.* everywhere in code instead of hard-coded strings.
    """

    # Course-level metadata
    C_INFO = "C_INFO"
    C_NAME = "C_NAME"
    C_LEVEL = "C_LEVEL"
    C_THEME = "C_THEME"
    C_DURATION = "C_DURATION"
    C_CODE = "C_CODE"
    C_DEV = "C_DEV"
    C_DESC = "C_DESC"

    # Learning objectives
    CLO = "CLO"

    # Scalar manager and structural IDs
    SCALEMGR = "SCALEMGR"
    SC_LESSON = "SC_LESSON"
    SC_TOPIC = "SC_TOPIC"
    SC_SUBTOPIC = "SC_SUBTOPIC"
    SC_PC = "SC_PC"

    # Content manager
    CONTMGR = "CONTMGR"
    CT_RESOURCE = "CT_RESOURCE"
    CT_TAG = "CT_TAG"
    CT_NOTE = "CT_NOTE"

    # Lesson manager & slide structure
    LSNMGR = "LSNMGR"
    SL_TITLE = "SL_TITLE"
    SL_SUBTITLE = "SL_SUBTITLE"
    SL_HEADING = "SL_HEADING"
    SL_SUBHEADING = "SL_SUBHEADING"
    SL_BODY = "SL_BODY"
    SL_BULLETS = "SL_BULLETS"
    SL_IMAGE = "SL_IMAGE"
    SL_QUOTE = "SL_QUOTE"
    SL_LABEL = "SL_LABEL"
    SL_TABLE = "SL_TABLE"

    # References
    REF_ENTRY = "REF_ENTRY"
    REF_AUTHOR = "REF_AUTHOR"
    REF_TITLE = "REF_TITLE"
    REF_YEAR = "REF_YEAR"
    REF_URL = "REF_URL"
    REF_TYPE = "REF_TYPE"

    # Assessments
    EX_Q = "EX_Q"
    EX_OPT = "EX_OPT"
    EX_KEY = "EX_KEY"
    EX_EXP = "EX_EXP"
    EX_DIFF = "EX_DIFF"
    EX_TOPIC = "EX_TOPIC"

    # Prometheus-specific system terms
    PKE_ENGINE = "PKE_ENGINE"
    PKE_TERM = "PKE_TERM"
    PKE_RESP = "PKE_RESP"
    TPL_MAP = "TPL_MAP"
    EXP_ENGINE = "EXP_ENGINE"
    SS_STATE = "SS_STATE"
    UI_PANEL = "UI_PANEL"
    UI_CONNECT = "UI_CONNECT"

    # Template / layout blocks for exports
    TPL_TITLE_BLOCK = "TPL_TITLE_BLOCK"
    TPL_SUBTITLE_BLOCK = "TPL_SUBTITLE_BLOCK"
    TPL_BODY = "TPL_BODY"
    TPL_BULLETS = "TPL_BULLETS"
    TPL_TABLE = "TPL_TABLE"
    TPL_IMAGE = "TPL_IMAGE"
    TPL_SLIDE_NO = "TPL_SLIDE_NO"
    TPL_FOOTER_LEFT = "TPL_FOOTER_LEFT"
    TPL_FOOTER_MID = "TPL_FOOTER_MID"
    TPL_FOOTER_RIGHT = "TPL_FOOTER_RIGHT"
    TPL_HEADER_LEFT = "TPL_HEADER_LEFT"
    TPL_HEADER_RIGHT = "TPL_HEADER_RIGHT"


# --------------------------------------------------------------------------- #
# Lexicon definition
# --------------------------------------------------------------------------- #


LEXICON: Dict[Lex, LexiconEntry] = {
    # -------------------- Course-level metadata ---------------------------- #
    Lex.C_INFO: LexiconEntry(
        id="C_INFO",
        primary_term="Course Information",
        variants=[
            "course information",
            "course info",
            "course details",
            "metadata",
        ],
        category="course",
        notes="Logical container for all course-level metadata.",
    ),
    Lex.C_NAME: LexiconEntry(
        id="C_NAME",
        primary_term="Course Title",
        variants=[
            "course title",
            "course name",
            "title",
            "name",
        ],
        category="course",
        notes="Display name of the course.",
    ),
    Lex.C_LEVEL: LexiconEntry(
        id="C_LEVEL",
        primary_term="Course Level",
        variants=[
            "course level",
            "level",
            "difficulty level",
        ],
        category="course",
        notes="Basic / Intermediate / Advanced / Executive / Custom.",
    ),
    Lex.C_THEME: LexiconEntry(
        id="C_THEME",
        primary_term="Thematic Area",
        variants=[
            "thematic",
            "theme",
            "thematic area",
            "category",
        ],
        category="course",
        notes="High-level subject or stream.",
    ),
    Lex.C_DURATION: LexiconEntry(
        id="C_DURATION",
        primary_term="Duration",
        variants=[
            "duration",
            "course duration",
            "length",
        ],
        category="course",
        notes="Recommended representation: integer days or '3 Days'.",
    ),
    Lex.C_CODE: LexiconEntry(
        id="C_CODE",
        primary_term="Course Code",
        variants=[
            "course code",
            "code",
            "identifier",
        ],
        category="course",
        notes="Optional external identifier.",
    ),
    Lex.C_DEV: LexiconEntry(
        id="C_DEV",
        primary_term="Developer Name",
        variants=[
            "developer",
            "developer name",
            "course developer",
            "author",
        ],
        category="course",
        notes="Name of the person or team responsible for the course.",
    ),
    Lex.C_DESC: LexiconEntry(
        id="C_DESC",
        primary_term="Course Description",
        variants=[
            "course description",
            "description",
            "overview",
            "summary",
        ],
        category="course",
        notes="Narrative summary; may be PKE-generated.",
    ),

    # -------------------- Learning objectives ----------------------------- #
    Lex.CLO: LexiconEntry(
        id="CLO",
        primary_term="Course Learning Objective",
        variants=[
            "clo",
            "clos",
            "lo",
            "los",
            "learning objective",
            "learning objectives",
            "course learning objective",
            "course learning objectives",
        ],
        category="structure",
        notes="CLO_n identifiers (CLO_1, CLO_2, etc.) derive from this root.",
    ),

    # -------------------- Scalar manager & structure ---------------------- #
    Lex.SCALEMGR: LexiconEntry(
        id="SCALEMGR",
        primary_term="Scalar Manager",
        variants=[
            "scalar",
            "scalar manager",
            "scalar table",
            "scalar index",
        ],
        category="structure",
        notes="Master structure for lesson, topic, subtopic, and PCs.",
    ),
    Lex.SC_LESSON: LexiconEntry(
        id="SC_LESSON",
        primary_term="Lesson Title",
        variants=[
            "lesson",
            "lesson title",
            "lesson name",
        ],
        category="structure",
        notes="First-level element in the scalar.",
    ),
    Lex.SC_TOPIC: LexiconEntry(
        id="SC_TOPIC",
        primary_term="Topic",
        variants=[
            "topic",
            "lesson topic",
            "module topic",
        ],
        category="structure",
        notes="Indexed as 1.1, 1.2, etc.",
    ),
    Lex.SC_SUBTOPIC: LexiconEntry(
        id="SC_SUBTOPIC",
        primary_term="Subtopic",
        variants=[
            "subtopic",
            "sub-topic",
            "element",
        ],
        category="structure",
        notes="Indexed as 1.1.1, 1.1.2, etc.",
    ),
    Lex.SC_PC: LexiconEntry(
        id="SC_PC",
        primary_term="Performance Criterion",
        variants=[
            "performance criterion",
            "performance criteria",
            "pc",
            "pcs",
            "performance measure",
        ],
        category="structure",
        notes="Usually associated with CLOs, topics, or subtopics.",
    ),

    # -------------------- Content manager -------------------------------- #
    Lex.CONTMGR: LexiconEntry(
        id="CONTMGR",
        primary_term="Content Manager",
        variants=[
            "content manager",
            "content hub",
            "resources manager",
        ],
        category="content",
        notes="Hub for resource ingestion and organisation.",
    ),
    Lex.CT_RESOURCE: LexiconEntry(
        id="CT_RESOURCE",
        primary_term="Resource",
        variants=[
            "resource",
            "file",
            "document",
            "attachment",
            "link",
            "media",
        ],
        category="content",
        notes="Unit of content (URL, image, PDF, etc.).",
    ),
    Lex.CT_TAG: LexiconEntry(
        id="CT_TAG",
        primary_term="Tag",
        variants=[
            "tag",
            "label",
            "descriptor",
        ],
        category="content",
        notes="Used for search and filtering.",
    ),
    Lex.CT_NOTE: LexiconEntry(
        id="CT_NOTE",
        primary_term="Content Note",
        variants=[
            "note",
            "annotation",
            "comment",
        ],
        category="content",
        notes="Free-text notes tied to a resource.",
    ),

    # -------------------- Lesson manager & slides ------------------------- #
    Lex.LSNMGR: LexiconEntry(
        id="LSNMGR",
        primary_term="Lesson Manager",
        variants=[
            "lesson manager",
            "lessons manager",
            "lesson builder",
        ],
        category="lessons",
        notes="Assembly of lessons, slides, notes, and timing.",
    ),
    Lex.SL_TITLE: LexiconEntry(
        id="SL_TITLE",
        primary_term="Slide Title",
        variants=[
            "slide title",
            "title block",
            "slide header",
        ],
        category="slide",
        notes="Primary title text on a slide.",
    ),
    Lex.SL_SUBTITLE: LexiconEntry(
        id="SL_SUBTITLE",
        primary_term="Slide Subtitle",
        variants=[
            "subtitle",
            "slide subtitle",
        ],
        category="slide",
        notes="Secondary subtitle text on a slide.",
    ),
    Lex.SL_HEADING: LexiconEntry(
        id="SL_HEADING",
        primary_term="Heading",
        variants=[
            "heading",
            "section header",
            "h1",
        ],
        category="slide",
        notes="Main in-slide section heading.",
    ),
    Lex.SL_SUBHEADING: LexiconEntry(
        id="SL_SUBHEADING",
        primary_term="Subheading",
        variants=[
            "subheading",
            "sub-heading",
            "h2",
        ],
        category="slide",
        notes="Secondary in-slide heading.",
    ),
    Lex.SL_BODY: LexiconEntry(
        id="SL_BODY",
        primary_term="Body Text",
        variants=[
            "body",
            "body text",
            "paragraph",
            "text",
        ],
        category="slide",
        notes="Narrative body text.",
    ),
    Lex.SL_BULLETS: LexiconEntry(
        id="SL_BULLETS",
        primary_term="Bullet List",
        variants=[
            "bullets",
            "bullet list",
            "bullet points",
            "list",
        ],
        category="slide",
        notes="One or more bullet items.",
    ),
    Lex.SL_IMAGE: LexiconEntry(
        id="SL_IMAGE",
        primary_term="Image",
        variants=[
            "image",
            "picture",
            "photo",
            "graphic",
        ],
        category="slide",
        notes="Single image on a slide.",
    ),
    Lex.SL_QUOTE: LexiconEntry(
        id="SL_QUOTE",
        primary_term="Quote",
        variants=[
            "quote",
            "pull quote",
            "highlight quote",
        ],
        category="slide",
        notes="Quotation or highlighted statement.",
    ),
    Lex.SL_LABEL: LexiconEntry(
        id="SL_LABEL",
        primary_term="Label",
        variants=[
            "label",
            "tag",
            "marker",
        ],
        category="slide",
        notes="Short text label for diagram elements, etc.",
    ),
    Lex.SL_TABLE: LexiconEntry(
        id="SL_TABLE",
        primary_term="Table",
        variants=[
            "table",
            "data table",
            "grid",
        ],
        category="slide",
        notes="Tabular data element.",
    ),

    # -------------------- References ------------------------------------- #
    Lex.REF_ENTRY: LexiconEntry(
        id="REF_ENTRY",
        primary_term="Reference Entry",
        variants=[
            "reference",
            "reference entry",
            "bibliography entry",
            "source",
        ],
        category="reference",
        notes="Single reference row.",
    ),
    Lex.REF_AUTHOR: LexiconEntry(
        id="REF_AUTHOR",
        primary_term="Author",
        variants=[
            "author",
            "authors",
        ],
        category="reference",
        notes="Primary author list.",
    ),
    Lex.REF_TITLE: LexiconEntry(
        id="REF_TITLE",
        primary_term="Reference Title",
        variants=[
            "title",
            "reference title",
        ],
        category="reference",
        notes="Title of the work.",
    ),
    Lex.REF_YEAR: LexiconEntry(
        id="REF_YEAR",
        primary_term="Publication Year",
        variants=[
            "year",
            "publication year",
            "date",
        ],
        category="reference",
        notes="Year of publication.",
    ),
    Lex.REF_URL: LexiconEntry(
        id="REF_URL",
        primary_term="Reference URL",
        variants=[
            "url",
            "link",
            "doi",
            "web address",
        ],
        category="reference",
        notes="Resolvable URL or DOI.",
    ),
    Lex.REF_TYPE: LexiconEntry(
        id="REF_TYPE",
        primary_term="Reference Type",
        variants=[
            "type",
            "source type",
            "format",
        ],
        category="reference",
        notes="Book, journal, website, etc.",
    ),

    # -------------------- Assessments ------------------------------------ #
    Lex.EX_Q: LexiconEntry(
        id="EX_Q",
        primary_term="Exam Question",
        variants=[
            "question",
            "exam question",
            "mcq",
            "item",
        ],
        category="assessment",
        notes="Single assessment question.",
    ),
    Lex.EX_OPT: LexiconEntry(
        id="EX_OPT",
        primary_term="Answer Option",
        variants=[
            "answer option",
            "option",
            "choice",
        ],
        category="assessment",
        notes="Single MCQ option.",
    ),
    Lex.EX_KEY: LexiconEntry(
        id="EX_KEY",
        primary_term="Correct Answer",
        variants=[
            "correct answer",
            "key",
            "answer key",
        ],
        category="assessment",
        notes="Identifier of the correct option.",
    ),
    Lex.EX_EXP: LexiconEntry(
        id="EX_EXP",
        primary_term="Explanation",
        variants=[
            "explanation",
            "rationale",
            "feedback",
        ],
        category="assessment",
        notes="Optional explanation or feedback.",
    ),
    Lex.EX_DIFF: LexiconEntry(
        id="EX_DIFF",
        primary_term="Difficulty",
        variants=[
            "difficulty",
            "difficulty level",
        ],
        category="assessment",
        notes="Simple difficulty tag (e.g. Easy/Med/Hard).",
    ),
    Lex.EX_TOPIC: LexiconEntry(
        id="EX_TOPIC",
        primary_term="Question Topic",
        variants=[
            "question topic",
            "topic",
        ],
        category="assessment",
        notes="Link back to a scalar topic/subtopic.",
    ),

    # -------------------- Prometheus system terms ------------------------ #
    Lex.PKE_ENGINE: LexiconEntry(
        id="PKE_ENGINE",
        primary_term="Prometheus Knowledge Engine",
        variants=[
            "pke",
            "prometheus ai",
            "ai engine",
        ],
        category="system",
        notes="Logical label for all AI-assisted operations.",
    ),
    Lex.PKE_TERM: LexiconEntry(
        id="PKE_TERM",
        primary_term="PKE Terminal",
        variants=[
            "ai terminal",
            "pke terminal",
            "ai chat window",
        ],
        category="system",
        notes="The gold interaction band on the main UI.",
    ),
    Lex.PKE_RESP: LexiconEntry(
        id="PKE_RESP",
        primary_term="PKE Response",
        variants=[
            "pke response",
            "ai response",
        ],
        category="system",
        notes="Block of text returned by the PKE.",
    ),
    Lex.TPL_MAP: LexiconEntry(
        id="TPL_MAP",
        primary_term="Template Map",
        variants=[
            "template map",
            "layout map",
            "field map",
        ],
        category="system",
        notes="Mapping between Lex IDs and template placeholders.",
    ),
    Lex.EXP_ENGINE: LexiconEntry(
        id="EXP_ENGINE",
        primary_term="Export Engine",
        variants=[
            "export engine",
            "generator",
            "exporter",
        ],
        category="system",
        notes="Generic term for PPTX/DOCX/XLSX generators.",
    ),
    Lex.SS_STATE: LexiconEntry(
        id="SS_STATE",
        primary_term="Session State",
        variants=[
            "session state",
            "ui state",
            "state",
        ],
        category="system",
        notes="Shared state across UI tabs.",
    ),
    Lex.UI_PANEL: LexiconEntry(
        id="UI_PANEL",
        primary_term="UI Panel",
        variants=[
            "panel",
            "window",
            "card",
        ],
        category="system",
        notes="Logical UI region in the layout.",
    ),
    Lex.UI_CONNECT: LexiconEntry(
        id="UI_CONNECT",
        primary_term="UI Connector",
        variants=[
            "connector",
            "flow line",
            "node connection",
        ],
        category="system",
        notes="Visual connector between panels/nodes.",
    ),

    # -------------------- Template / layout terms ------------------------ #
    Lex.TPL_TITLE_BLOCK: LexiconEntry(
        id="TPL_TITLE_BLOCK",
        primary_term="Template Title Block",
        variants=[
            "title block",
            "ppt title",
            "slide title placeholder",
        ],
        category="template",
        notes="Placeholder in template for slide titles.",
    ),
    Lex.TPL_SUBTITLE_BLOCK: LexiconEntry(
        id="TPL_SUBTITLE_BLOCK",
        primary_term="Template Subtitle Block",
        variants=[
            "subtitle block",
            "ppt subtitle",
        ],
        category="template",
        notes="Placeholder for slide subtitles.",
    ),
    Lex.TPL_BODY: LexiconEntry(
        id="TPL_BODY",
        primary_term="Template Body Text",
        variants=[
            "body block",
            "content block",
            "text placeholder",
        ],
        category="template",
        notes="General body text placeholder.",
    ),
    Lex.TPL_BULLETS: LexiconEntry(
        id="TPL_BULLETS",
        primary_term="Template Bullet Block",
        variants=[
            "bullet block",
            "bullets placeholder",
        ],
        category="template",
        notes="Bullet text placeholder.",
    ),
    Lex.TPL_TABLE: LexiconEntry(
        id="TPL_TABLE",
        primary_term="Template Table Block",
        variants=[
            "table block",
            "table placeholder",
        ],
        category="template",
        notes="Tabular placeholder region.",
    ),
    Lex.TPL_IMAGE: LexiconEntry(
        id="TPL_IMAGE",
        primary_term="Template Image Block",
        variants=[
            "image block",
            "picture placeholder",
        ],
        category="template",
        notes="Image placeholder region.",
    ),
    Lex.TPL_SLIDE_NO: LexiconEntry(
        id="TPL_SLIDE_NO",
        primary_term="Template Slide Number",
        variants=[
            "slide number",
            "slide no",
        ],
        category="template",
        notes="Slide number display field.",
    ),
    Lex.TPL_FOOTER_LEFT: LexiconEntry(
        id="TPL_FOOTER_LEFT",
        primary_term="Footer Left",
        variants=[
            "footer left",
            "left footer",
        ],
        category="template",
        notes="Left footer text placeholder.",
    ),
    Lex.TPL_FOOTER_MID: LexiconEntry(
        id="TPL_FOOTER_MID",
        primary_term="Footer Centre",
        variants=[
            "footer middle",
            "footer centre",
            "footer center",
        ],
        category="template",
        notes="Middle footer text placeholder.",
    ),
    Lex.TPL_FOOTER_RIGHT: LexiconEntry(
        id="TPL_FOOTER_RIGHT",
        primary_term="Footer Right",
        variants=[
            "footer right",
            "right footer",
        ],
        category="template",
        notes="Right footer text placeholder.",
    ),
    Lex.TPL_HEADER_LEFT: LexiconEntry(
        id="TPL_HEADER_LEFT",
        primary_term="Header Left",
        variants=[
            "header left",
            "left header",
        ],
        category="template",
        notes="Left header placeholder.",
    ),
    Lex.TPL_HEADER_RIGHT: LexiconEntry(
        id="TPL_HEADER_RIGHT",
        primary_term="Header Right",
        variants=[
            "header right",
            "right header",
        ],
        category="template",
        notes="Right header placeholder.",
    ),
}


# Build a fast lookup from normalised variant -> Lex ID
_VARIANT_INDEX: Dict[str, Lex] = {}


def _normalise_key(value: str) -> str:
    """Normalise a human string for variant lookup.

    Lowercase, strip spaces, underscores, hyphens, and colons.
    """
    v = value.strip().lower()
    for ch in (" ", "_", "-", ":", "."):
        v = v.replace(ch, "")
    return v


for lex_id, entry in LEXICON.items():
    # Primary term
    _VARIANT_INDEX[_normalise_key(entry.primary_term)] = lex_id
    # Variants
    for v in entry.variants:
        _VARIANT_INDEX[_normalise_key(v)] = lex_id
    # Also index the raw ID string itself
    _VARIANT_INDEX[_normalise_key(entry.id)] = lex_id


# --------------------------------------------------------------------------- #
# Public helpers
# --------------------------------------------------------------------------- #


def normalise_term(term_or_id: str) -> Optional[Lex]:
    """Return the canonical Lex ID for a raw label or ID string.

    Examples:
        normalise_term("Course Name") -> Lex.C_NAME
        normalise_term("clo 1")       -> Lex.CLO (root)
        normalise_term("SLIDE TITLE") -> Lex.SL_TITLE
    """
    key = _normalise_key(term_or_id)
    return _VARIANT_INDEX.get(key)


def get_entry(term_or_id: str | Lex) -> Optional[LexiconEntry]:
    """Return the LexiconEntry for a given Lex ID or user-facing term."""
    if isinstance(term_or_id, Lex):
        return LEXICON.get(term_or_id)
    lex = normalise_term(str(term_or_id))
    if lex is None:
        return None
    return LEXICON.get(lex)


def is_term(term_or_id: str | Lex, expected: Lex) -> bool:
    """True if the given value resolves to the expected Lex ID."""
    if isinstance(term_or_id, Lex):
        return term_or_id is expected
    lex = normalise_term(str(term_or_id))
    return lex is expected
