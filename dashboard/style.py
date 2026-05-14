import streamlit as st


def apply_dashboard_style() -> None:
    st.markdown(
        """
        <style>
            :root {
                --app-bg: #f8fafc;
                --surface: #ffffff;
                --surface-soft: #eef2ff;
                --border: #d7dde8;
                --text: #111827;
                --muted: #4b5563;
                --accent: #2563eb;
                --accent-strong: #1d4ed8;
            }

            .stApp {
                background-color: var(--app-bg);
                color: var(--text);
            }

            .block-container {
                padding-top: 1.25rem;
                padding-bottom: 1.5rem;
                max-width: 1320px;
            }

            h1, h2, h3, h4, h5, h6,
            p, li, span, label, div {
                color: var(--text);
            }

            h1 {
                letter-spacing: 0;
                margin-bottom: 0.1rem;
            }

            h2, h3 {
                letter-spacing: 0;
                margin-top: 1.1rem;
                margin-bottom: 0.65rem;
            }

            [data-testid="stCaptionContainer"],
            [data-testid="stCaptionContainer"] * {
                color: var(--muted) !important;
                opacity: 1 !important;
            }

            section[data-testid="stSidebar"] {
                border-right: 1px solid var(--border);
                background-color: #f1f5f9;
            }

            section[data-testid="stSidebar"] * {
                color: var(--text) !important;
            }

            div[data-testid="stWidgetLabel"] {
                opacity: 1 !important;
            }

            div[data-testid="stWidgetLabel"] label {
                color: var(--muted) !important;
                font-weight: 600 !important;
                opacity: 1 !important;
            }

            div[data-testid="stMetric"] {
                background: var(--surface);
                border: 1px solid var(--border);
                border-radius: 8px;
                padding: 1rem 1.2rem;
                box-shadow: 0 1px 2px rgba(15, 23, 42, 0.08);
                min-height: 126px;
            }

            div[data-testid="stMetricLabel"],
            div[data-testid="stMetricLabel"] *,
            div[data-testid="stMetricLabel"] label,
            div[data-testid="stMetricLabel"] p {
                color: #374151 !important;
                fill: #374151 !important;
                opacity: 1 !important;
                font-weight: 700 !important;
                font-size: 0.95rem;
                line-height: 1.25;
                white-space: normal !important;
                visibility: visible !important;
            }

            div[data-testid="stMetricValue"],
            div[data-testid="stMetricValue"] *,
            div[data-testid="stMetricValue"] p {
                color: var(--text) !important;
                opacity: 1 !important;
                font-size: clamp(1.45rem, 2.4vw, 2.65rem);
                font-weight: 800 !important;
                line-height: 1.12;
                white-space: normal !important;
                overflow-wrap: anywhere;
                word-break: break-word;
                overflow: visible !important;
                text-overflow: clip !important;
            }

            div[data-testid="stMetricDelta"],
            div[data-testid="stMetricDelta"] *,
            div[data-testid="stMetricDelta"] p {
                font-weight: 700 !important;
                color: var(--muted) !important;
                opacity: 1 !important;
                white-space: normal !important;
            }

            [data-testid="stAlert"] {
                border-radius: 8px;
                border: 1px solid var(--border);
            }

            [data-testid="stExpander"] {
                border: 1px solid var(--border);
                border-radius: 8px;
                background: var(--surface);
            }

            [data-testid="stExpander"] details summary p {
                font-weight: 650;
                color: var(--text) !important;
            }

            [data-testid="stDataFrame"] {
                border: 1px solid var(--border);
                border-radius: 8px;
            }

            div[data-baseweb="select"] > div {
                background-color: var(--surface) !important;
                color: var(--text) !important;
                border: 1px solid var(--border) !important;
                border-radius: 8px !important;
            }

            div[data-baseweb="select"] *,
            div[data-baseweb="select"] input {
                color: var(--text) !important;
                opacity: 1 !important;
            }

            div[data-baseweb="popover"],
            div[data-baseweb="popover"] *,
            div[data-baseweb="menu"],
            div[data-baseweb="menu"] *,
            ul[data-baseweb="menu"],
            ul[data-baseweb="menu"] *,
            div[role="listbox"],
            div[role="listbox"] *,
            ul[role="listbox"],
            ul[role="listbox"] * {
                background-color: var(--surface) !important;
                color: var(--text) !important;
                opacity: 1 !important;
            }

            div[role="option"],
            div[role="option"] *,
            li[role="option"],
            li[role="option"] * {
                background-color: var(--surface) !important;
                color: var(--text) !important;
                opacity: 1 !important;
                font-weight: 600 !important;
            }

            div[role="option"]:hover,
            div[role="option"][aria-selected="true"],
            li[role="option"]:hover,
            li[role="option"][aria-selected="true"] {
                background-color: var(--surface-soft) !important;
                color: var(--text) !important;
            }

            div[data-baseweb="popover"] {
                border: 1px solid var(--border) !important;
                border-radius: 8px !important;
                box-shadow: 0 12px 24px rgba(15, 23, 42, 0.16) !important;
            }

            [data-baseweb="tag"] {
                background-color: #dbeafe !important;
                border: 1px solid #93c5fd !important;
                color: var(--text) !important;
                border-radius: 7px !important;
            }

            [data-baseweb="tag"] span,
            [data-baseweb="tag"] svg {
                color: var(--text) !important;
                fill: var(--text) !important;
            }

            [role="radio"] > div:first-child {
                border-color: var(--accent) !important;
            }

            [role="radio"][aria-checked="true"] > div:first-child {
                background-color: var(--accent) !important;
            }

            .stSlider [data-baseweb="slider"] div {
                color: var(--accent) !important;
            }

            .stButton > button,
            [data-testid="stFormSubmitButton"] button {
                background: var(--accent) !important;
                color: #ffffff !important;
                border: 1px solid var(--accent-strong) !important;
                border-radius: 8px !important;
                font-weight: 700 !important;
            }

            .stButton > button:hover,
            [data-testid="stFormSubmitButton"] button:hover {
                background: var(--accent-strong) !important;
                border-color: var(--accent-strong) !important;
            }

            [data-testid="stForm"] {
                border: 1px solid var(--border);
                border-radius: 8px;
                background: var(--surface);
                padding: 1rem;
            }

            [data-testid="stTabs"] button p {
                color: var(--muted) !important;
                font-weight: 650;
            }

            [data-testid="stTabs"] button[aria-selected="true"] p {
                color: var(--accent-strong) !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
