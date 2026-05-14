import plotly.graph_objects as go


SEQUENTIAL_SCALE = [
    [0.0, "#93c5fd"],
    [0.45, "#3b82f6"],
    [1.0, "#1e3a8a"],
]

DIVERGING_SCALE = [
    [0.0, "#92400e"],
    [0.48, "#d97706"],
    [0.5, "#64748b"],
    [0.52, "#60a5fa"],
    [1.0, "#1d4ed8"],
]


def apply_chart_style(fig):
    fig.update_layout(
        margin=dict(l=36, r=36, t=52, b=44),
        legend_title_text="",
        font=dict(color="#111827", size=13),
        legend=dict(font=dict(color="#111827", size=13), bgcolor="rgba(255,255,255,0.88)"),
        hoverlabel=dict(bgcolor="white", bordercolor="#d1d5db", font_size=13, font_color="#111827"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        coloraxis_colorbar=dict(tickfont=dict(color="#111827"), title_font=dict(color="#111827")),
    )
    fig.update_xaxes(
        color="#111827",
        gridcolor="#e5e7eb",
        zerolinecolor="#9ca3af",
        title_font=dict(color="#374151"),
        tickfont=dict(color="#111827", size=12),
        linecolor="#cbd5e1",
        tickcolor="#94a3b8",
        automargin=True,
    )
    fig.update_yaxes(
        color="#111827",
        gridcolor="#e5e7eb",
        zerolinecolor="#9ca3af",
        title_font=dict(color="#374151"),
        tickfont=dict(color="#111827", size=12),
        linecolor="#cbd5e1",
        tickcolor="#94a3b8",
        automargin=True,
    )
    fig.update_traces(
        textfont=dict(color="#111827", size=12),
        marker_line_color="#1e3a8a",
        marker_line_width=0.7,
        selector=dict(type="bar"),
    )
    fig.update_traces(
        textfont=dict(color="#111827", size=12),
        marker_line_color="#1e3a8a",
        marker_line_width=0.4,
        selector=dict(type="histogram"),
    )
    return fig


def confidence_gauge(probability: float) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=probability * 100,
            number={"suffix": "%", "font": {"size": 30, "color": "#111827"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#111827", "tickfont": {"color": "#111827"}},
                "bar": {"color": "#2563eb", "line": {"color": "#1e3a8a", "width": 1}},
                "bgcolor": "#ffffff",
                "bordercolor": "#cbd5e1",
                "borderwidth": 1,
                "steps": [
                    {"range": [0, 50], "color": "#fed7aa"},
                    {"range": [50, 80], "color": "#bfdbfe"},
                    {"range": [80, 100], "color": "#93c5fd"},
                ],
                "threshold": {
                    "line": {"color": "#111827", "width": 3},
                    "thickness": 0.75,
                    "value": 50,
                },
            },
        )
    )
    fig.update_layout(
        height=260,
        margin=dict(l=18, r=18, t=24, b=18),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(color="#111827"),
    )
    return fig
