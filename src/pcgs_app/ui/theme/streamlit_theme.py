"""
Streamlit Theme Helpers

Applies the shared design tokens to Streamlit widgets/layout.
"""

from typing import Optional

import streamlit as st

from .tokens import ThemeTokens, get_default_tokens


def apply_base_theme(theme_tokens: Optional[ThemeTokens] = None) -> None:
    """
    Inject the base CSS that establishes the sci-fi neural map styling.
    """

    theme = theme_tokens or get_default_tokens()

    css = f"""
    <style>
    :root {{
        --pcgs-bg-main: {theme.bg_main};
        --pcgs-bg-panel: {theme.bg_panel};
        --pcgs-bg-panel-subtle: {theme.bg_panel_subtle};
        --pcgs-accent-primary: {theme.accent_primary};
        --pcgs-accent-secondary: {theme.accent_secondary};
        --pcgs-accent-warning: {theme.accent_warning};
        --pcgs-accent-error: {theme.accent_error};
        --pcgs-accent-success: {theme.accent_success};
        --pcgs-text-primary: {theme.text_primary};
        --pcgs-text-muted: {theme.text_muted};
        --pcgs-text-ai: {theme.text_ai};
        --pcgs-glow-ai: {theme.glow_ai};
        --pcgs-glow-progress: {theme.glow_progress};
        --pcgs-font-heading: '{theme.font_heading}', 'Segoe UI', sans-serif;
        --pcgs-font-body: '{theme.font_body}', 'Segoe UI', sans-serif;
        --pcgs-font-mono: '{theme.font_mono}', 'SFMono-Regular', monospace;
    }}

    body, .main, .block-container {{
        background: {theme.bg_main};
        color: var(--pcgs-text-primary);
        font-family: var(--pcgs-font-body);
    }}

    [data-testid="stAppViewContainer"] {{
        background: radial-gradient(circle at 20% 15%, rgba(44, 240, 255, 0.12), transparent 55%),
                    radial-gradient(circle at 80% 10%, rgba(124, 255, 175, 0.14), transparent 45%),
                    linear-gradient(145deg, #01030B 0%, #040B18 45%, #02030C 100%);
    }}

    .block-container {{
        padding-top: 0;
        padding-bottom: 2.5rem;
    }}

    .pcgs-root {{
        max-width: 96vw;
        margin: 1rem auto 2.75rem auto;
        padding: 1.5rem 2rem 2.6rem;
        background: radial-gradient(circle at top left, rgba(44, 240, 255, 0.12), transparent 40%),
                    linear-gradient(180deg, rgba(5, 12, 28, 0.98), rgba(3, 5, 12, 0.95));
        border: 1px solid rgba(44, 240, 255, 0.25);
        box-shadow: 0 0 45px rgba(17, 167, 199, 0.35);
        border-radius: 28px;
        display: grid;
        gap: 1.15rem 1.35rem;
        grid-template-columns: minmax(270px, 1fr) minmax(420px, 1.65fr) minmax(220px, 0.9fr);
        grid-template-areas:
            "status status status"
            "select course-info generate"
            "learning course-desc generate"
            "learning course-desc generate"
            ". connectors ."
            "managers managers managers"
            "ai ai ai"
            "footer footer footer";
        grid-auto-rows: minmax(min-content, auto);
    }}

    .pcgs-root > div[data-testid="stVerticalBlock"] {{
        display: contents;
    }}

    .pcgs-region-status {{ grid-area: status; }}
    .pcgs-region-select {{ grid-area: select; }}
    .pcgs-region-learning {{
        grid-area: learning;
        min-height: 0;
        display: flex;
    }}
    .pcgs-region-learning > .pcgs-panel {{
        width: 100%;
    }}
    .pcgs-region-course-info {{
        grid-area: course-info;
        min-height: 0;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }}
    .pcgs-region-course-desc {{
        grid-area: course-desc;
        min-height: 0;
        display: flex;
        flex-direction: column;
    }}
    .pcgs-region-generate {{
        grid-area: generate;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        min-height: 0;
    }}
    .pcgs-region-connectors {{
        grid-area: connectors;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0 2rem;
        min-height: 60px;
    }}
    .pcgs-region-managers {{ grid-area: managers; }}
    .pcgs-region-ai {{
        grid-area: ai;
        display: flex;
    }}
    .pcgs-region-ai > .pcgs-ai-band {{
        width: 100%;
    }}
    .pcgs-region-footer {{ grid-area: footer; }}

    .pcgs-region-select,
    .pcgs-region-learning,
    .pcgs-region-course-info,
    .pcgs-region-course-desc,
    .pcgs-region-generate,
    .pcgs-region-connectors,
    .pcgs-region-managers,
    .pcgs-region-ai,
    .pcgs-region-footer {{
        position: relative;
        min-height: 0;
    }}

    .pcgs-status-band {{
        display: grid;
        grid-template-columns: minmax(420px, 2fr) minmax(220px, 0.9fr);
        gap: 1.35rem;
        background: rgba(5, 10, 22, 0.92);
        border: 1px solid rgba(44, 240, 255, 0.35);
        border-radius: 26px;
        padding: 1.4rem 1.75rem;
        box-shadow: inset 0 0 35px rgba(44, 240, 255, 0.12), 0 6px 35px rgba(0, 0, 0, 0.45);
    }}

    .pcgs-status-band__left {{
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}

    .pcgs-status-band__right {{
        display: flex;
        justify-content: flex-end;
        align-items: flex-start;
    }}

    @media (max-width: 1400px) {{
        .pcgs-root {{
            grid-template-columns: minmax(240px, 1fr) minmax(360px, 1.4fr) minmax(200px, 0.8fr);
        }}
        .pcgs-status-band {{
            grid-template-columns: minmax(320px, 1fr) minmax(200px, 0.8fr);
        }}
    }}

    .pcgs-header-status {{
        display: flex;
        flex-direction: column;
        gap: 0.55rem;
    }}

    .pcgs-header-status__title {{
        font-size: 1.05rem;
        text-transform: uppercase;
        letter-spacing: 0.35em;
        margin: 0;
        font-weight: 700;
    }}

    .pcgs-header-status__timestamp {{
        font-family: var(--pcgs-font-mono);
        color: rgba(124, 255, 182, 0.8);
        font-size: 0.9rem;
        letter-spacing: 0.2em;
    }}

    .pcgs-header-status__metrics {{
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
        font-size: 0.95rem;
        color: #7CFFB6;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.08em;
    }}

    .pcgs-top-buttons {{
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 0.55rem;
        min-width: 280px;
    }}

    .pcgs-top-buttons .pcgs-pill-button {{
        width: 100%;
        min-width: 180px;
    }}

    .pcgs-select-course {{
        margin: 0;
        padding: 1rem 1.5rem;
        border-radius: 18px;
        border: 1px dashed rgba(44, 240, 255, 0.55);
        background: rgba(6, 12, 24, 0.7);
    }}

    .pcgs-panel {{
        background: var(--pcgs-bg-panel);
        border-radius: 22px;
        border: 1px solid rgba(44, 240, 255, 0.25);
        box-shadow: 0 12px 35px rgba(1, 3, 11, 0.85);
        padding: 1.5rem;
        margin-bottom: 0.75rem;
        position: relative;
        overflow: hidden;
    }}

    .pcgs-panel--course-info,
    .pcgs-panel--description,
    .pcgs-panel--clos,
    .pcgs-panel--export {{
        background: linear-gradient(180deg, rgba(8, 14, 28, 0.96), rgba(4, 6, 12, 0.93));
    }}

    .pcgs-panel--clos {{
        display: flex;
        flex-direction: column;
        height: 100%;
    }}

    .pcgs-panel--clos .pcgs-clos-list {{
        flex: 1;
        min-height: 0;
        max-height: none;
        overflow-y: auto;
    }}

    .pcgs-panel--unsaved {{
        border-color: rgba(247, 227, 116, 0.8);
        box-shadow: 0 0 25px rgba(247, 227, 116, 0.25);
        animation: pcgs-unsaved 2.6s infinite;
    }}

    @keyframes pcgs-unsaved {{
        0% {{ box-shadow: 0 0 20px rgba(247, 227, 116, 0.15); }}
        50% {{ box-shadow: 0 0 28px rgba(247, 227, 116, 0.4); }}
        100% {{ box-shadow: 0 0 20px rgba(247, 227, 116, 0.15); }}
    }}

    .pcgs-panel--ai-target {{
        border-color: rgba(255, 179, 71, 0.95);
        box-shadow: 0 0 35px rgba(255, 179, 71, 0.4);
        animation: pcgs-ai-target 1.8s infinite alternate;
    }}

    .pcgs-panel--complete {{
        border-color: rgba(124, 255, 175, 0.85);
        box-shadow: 0 0 28px rgba(124, 255, 175, 0.25);
    }}

    .pcgs-panel--disabled {{
        opacity: 0.45;
        pointer-events: none;
    }}

    @keyframes pcgs-ai-target {{
        from {{ box-shadow: 0 0 20px rgba(255, 179, 71, 0.2); }}
        to {{ box-shadow: 0 0 32px rgba(255, 179, 71, 0.45); }}
    }}

    .pcgs-panel__header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem;
        margin-bottom: 1.1rem;
    }}

    .pcgs-panel__title {{
        font-family: var(--pcgs-font-heading);
        letter-spacing: 0.25em;
        font-size: 0.95rem;
        text-transform: uppercase;
        color: var(--pcgs-text-muted);
        display: flex;
        align-items: center;
        gap: 0.45rem;
    }}

    .pcgs-panel__subtitle {{
        font-size: 0.8rem;
        letter-spacing: 0.08em;
        color: var(--pcgs-text-muted);
    }}

    .pcgs-panel__actions {{
        display: flex;
        align-items: center;
        gap: 0.45rem;
    }}

    .pcgs-flame-button {{
        width: 46px;
        height: 46px;
        border-radius: 50%;
        border: 1px solid rgba(255, 179, 71, 0.6);
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(255, 179, 71, 0.08);
        box-shadow: 0 0 18px rgba(255, 179, 71, 0.25);
    }}

    .pcgs-flame-button button {{
        background: transparent;
        border: none;
        font-size: 1.25rem;
        color: #FFB347;
        width: 100%;
        height: 100%;
        cursor: pointer;
    }}

    .pcgs-mini-button {{
        width: 36px;
        height: 36px;
        border-radius: 50%;
        border: 1px solid rgba(44, 240, 255, 0.45);
        background: rgba(44, 240, 255, 0.08);
        color: var(--pcgs-text-primary);
        font-size: 1rem;
        text-align: center;
        box-shadow: 0 0 15px rgba(44, 240, 255, 0.2);
    }}

    .pcgs-course-info-grid {{
        display: grid;
        gap: 1rem;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    }}

    .pcgs-pill-button {{
        border-radius: 999px;
        padding: 2px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        background: rgba(255, 255, 255, 0.05);
        box-shadow: inset 0 0 15px rgba(255, 255, 255, 0.05);
    }}

    .pcgs-pill-button button {{
        border-radius: 999px;
        width: 100%;
        height: 44px;
        border: none;
        background: transparent;
        color: var(--pcgs-text-primary);
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        cursor: pointer;
    }}

    .pcgs-pill-button--primary {{
        border-color: rgba(44, 240, 255, 0.75);
    }}

    .pcgs-pill-button--primary button {{
        color: var(--pcgs-accent-primary);
    }}

    .pcgs-pill-button--neutral button {{
        color: var(--pcgs-text-primary);
    }}

    .pcgs-pill-button--danger {{
        border-color: rgba(255, 77, 109, 0.8);
    }}

    .pcgs-pill-button--danger button {{
        color: var(--pcgs-accent-error);
    }}

    .pcgs-clos-list {{
        flex: 1;
        min-height: 0;
        overflow-y: auto;
        padding-right: 0.5rem;
    }}

    .pcgs-clos-item {{
        margin-bottom: 0.75rem;
        padding: 0.9rem;
        border-radius: 14px;
        background: rgba(6, 12, 21, 0.7);
        border: 1px solid rgba(44, 240, 255, 0.15);
    }}

    .pcgs-generate-buttons {{
        display: flex;
        flex-direction: column;
        gap: 0.8rem;
    }}

    .pcgs-generate-buttons .pcgs-pill-button button {{
        height: 52px;
        font-size: 0.85rem;
    }}

    .pcgs-region-generate .pcgs-panel {{
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }}

    .pcgs-region-generate .pcgs-generate-buttons {{
        margin-top: 0.5rem;
        flex: 1;
        justify-content: center;
    }}

    .pcgs-region-generate .pcgs-pill-button {{
        border-color: rgba(44, 240, 255, 0.65);
        background: rgba(44, 240, 255, 0.08);
        box-shadow: 0 0 25px rgba(44, 240, 255, 0.2);
    }}

    .pcgs-region-generate .pcgs-pill-button button {{
        color: #F7FCFF;
        font-size: 0.92rem;
    }}

    .pcgs-node-row {{
        display: grid;
        gap: 1.1rem;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    }}

    .pcgs-managers-row {{
        margin: 0;
    }}

    .pcgs-managers-row + .pcgs-ai-band {{
        margin-top: 0;
    }}

    .pcgs-node-tile {{
        border-radius: 20px;
        border: 1px solid rgba(44, 240, 255, 0.35);
        padding: 1.25rem;
        box-shadow: 0 0 25px rgba(44, 240, 255, 0.15);
        background: linear-gradient(180deg, rgba(5, 10, 19, 0.95), rgba(3, 6, 12, 0.93));
    }}

    .pcgs-node-tile--idle {{
        opacity: 0.82;
    }}

    .pcgs-node-tile--in-progress {{
        border-color: rgba(247, 227, 116, 0.7);
        box-shadow: 0 0 25px rgba(247, 227, 116, 0.2);
    }}

    .pcgs-node-tile--complete {{
        border-color: rgba(98, 255, 183, 0.85);
        box-shadow: 0 0 25px rgba(124, 255, 175, 0.25);
    }}

    .pcgs-node-tile--ai-target {{
        border-color: rgba(255, 179, 71, 0.85);
        box-shadow: 0 0 30px rgba(255, 179, 71, 0.25);
    }}

    .pcgs-node-tile button {{
        width: 100%;
        border-radius: 16px;
        border: 1px solid rgba(44, 240, 255, 0.3);
        background: rgba(6, 12, 21, 0.8);
        color: var(--pcgs-text-primary);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        padding: 0.9rem;
        cursor: pointer;
    }}

    .pcgs-node-tile__meta {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.75rem;
    }}

    .pcgs-connector-row {{
        display: flex;
        gap: 1rem;
        width: 100%;
        max-width: 640px;
        margin: 0;
        justify-content: center;
    }}

    .pcgs-connector {{
        flex: 1;
        height: 3px;
        background: rgba(44, 240, 255, 0.35);
        border-radius: 999px;
        box-shadow: 0 0 18px rgba(44, 240, 255, 0.15);
    }}

    .pcgs-connector--vertical {{
        width: 3px;
        height: 48px;
        margin: 0 auto;
        background: rgba(44, 240, 255, 0.25);
    }}

    .pcgs-connector--idle {{
        opacity: 0.25;
    }}

    .pcgs-connector--active {{
        background: linear-gradient(90deg, transparent, var(--pcgs-accent-primary), transparent);
        box-shadow: 0 0 20px rgba(44, 240, 255, 0.45);
    }}

    .pcgs-connector--complete {{
        background: var(--pcgs-accent-primary);
        box-shadow: 0 0 24px rgba(44, 240, 255, 0.5);
    }}

    .pcgs-ai-band {{
        margin-top: 0;
        padding: 1.5rem;
        border-radius: 22px;
        border: 1px solid rgba(255, 179, 71, 0.4);
        background: linear-gradient(120deg, rgba(255, 221, 158, 0.35), rgba(112, 83, 28, 0.2));
        color: var(--pcgs-text-ai);
        font-family: var(--pcgs-font-mono);
        box-shadow: inset 0 0 35px rgba(255, 179, 71, 0.2);
    }}

    .pcgs-ai-band--active {{
        border-color: rgba(255, 179, 71, 0.85);
        box-shadow: 0 0 35px rgba(255, 179, 71, 0.35), inset 0 0 35px rgba(255, 179, 71, 0.25);
    }}

    .pcgs-ai-band__feed {{
        max-height: 220px;
        overflow-y: auto;
        margin-bottom: 1rem;
    }}

    .pcgs-ai-band__line {{
        margin-bottom: 0.4rem;
        letter-spacing: 0.05em;
        color: var(--pcgs-text-ai);
    }}

    .pcgs-ai-band__speaker {{
        color: rgba(27, 18, 2, 0.75);
        background: rgba(255, 255, 255, 0.35);
        border-radius: 6px;
        padding: 0 0.4rem;
        margin-right: 0.5rem;
    }}

    .pcgs-ai-band__prompt {{
        text-transform: uppercase;
        letter-spacing: 0.15em;
        font-size: 0.75rem;
        margin-bottom: 0.35rem;
        color: rgba(31, 19, 2, 0.8);
    }}

    .pcgs-ai-band input {{
        font-family: var(--pcgs-font-mono);
        background: rgba(0, 0, 0, 0.35);
        border: 1px solid rgba(255, 179, 71, 0.6);
        color: var(--pcgs-text-ai);
    }}

    .pcgs-ai-band__caret {{
        display: inline-block;
        width: 10px;
        height: 18px;
        background: var(--pcgs-text-ai);
        animation: pcgs-caret 1s infinite;
        margin-left: 4px;
    }}

    @keyframes pcgs-caret {{
        0%, 50% {{ opacity: 1; }}
        51%, 100% {{ opacity: 0; }}
    }}

    .pcgs-status-dot {{
        width: 10px;
        height: 10px;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px currentColor;
    }}

    .pcgs-status-dot--ok {{
        color: var(--pcgs-accent-success);
    }}

    .pcgs-status-dot--warn {{
        color: var(--pcgs-accent-warning);
    }}

    .pcgs-status-dot--error {{
        color: var(--pcgs-accent-error);
    }}

    .pcgs-status-dot--idle {{
        color: rgba(255, 255, 255, 0.35);
    }}

    .pcgs-progress {{
        width: 100%;
        height: 6px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.1);
        overflow: hidden;
        margin-top: 0.4rem;
    }}

    .pcgs-progress__value {{
        height: 100%;
        background: linear-gradient(90deg, rgba(10, 226, 199, 0.2), var(--pcgs-glow-progress));
        box-shadow: 0 0 15px rgba(124, 255, 175, 0.45);
        border-radius: 999px;
    }}
    .pcgs-footer {{
        margin-top: 0;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 0.5rem 1.5rem;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 0.12em;
        color: var(--pcgs-text-muted);
    }}

    .pcgs-footer strong {{
        color: var(--pcgs-text-primary);
    }}

    .pcgs-root .stTextInput input,
    .pcgs-root .stTextArea textarea,
    .pcgs-root .stNumberInput input {{
        background: rgba(2, 6, 16, 0.95);
        border: 1px solid rgba(44, 240, 255, 0.35);
        color: var(--pcgs-text-primary);
        font-family: var(--pcgs-font-body);
        border-radius: 10px;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }}

    .pcgs-root .stTextInput input:focus,
    .pcgs-root .stTextArea textarea:focus,
    .pcgs-root .stNumberInput input:focus {{
        border-color: var(--pcgs-accent-primary);
        box-shadow: 0 0 0 1px var(--pcgs-accent-primary);
        outline: none;
    }}

    .pcgs-root .stTextInput input::placeholder,
    .pcgs-root .stTextArea textarea::placeholder {{
        color: rgba(255, 255, 255, 0.35);
    }}

    .pcgs-root .stSelectbox [data-baseweb="select"] > div,
    .pcgs-root .stSelectbox [role="combobox"] {{
        background: rgba(2, 6, 16, 0.95) !important;
        border: 1px solid rgba(44, 240, 255, 0.35) !important;
        color: var(--pcgs-text-primary) !important;
        border-radius: 10px !important;
        min-height: 48px;
    }}

    .pcgs-root .stSelectbox [data-baseweb="select"] > div:focus-within,
    .pcgs-root .stSelectbox [role="combobox"]:focus {{
        border-color: var(--pcgs-accent-primary) !important;
        box-shadow: 0 0 0 1px var(--pcgs-accent-primary) !important;
        outline: none !important;
    }}

    .pcgs-root .stSelectbox svg {{
        color: var(--pcgs-accent-primary);
    }}

    .pcgs-root .stButton button {{
        background: rgba(4, 8, 18, 0.85);
        border: 1px solid rgba(44, 240, 255, 0.45);
        color: var(--pcgs-text-primary);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        border-radius: 999px;
        transition: border-color 0.2s ease, color 0.2s ease, box-shadow 0.2s ease;
    }}

    .pcgs-root .stButton button:hover,
    .pcgs-root .stButton button:focus {{
        border-color: var(--pcgs-accent-primary);
        color: var(--pcgs-accent-primary);
        box-shadow: 0 0 12px rgba(44, 240, 255, 0.35);
    }}

    .pcgs-root .stButton button:disabled {{
        opacity: 0.5;
        border-color: rgba(255, 255, 255, 0.15);
        color: rgba(255, 255, 255, 0.55);
    }}
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)

