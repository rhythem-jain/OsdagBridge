"""Shared visual settings for the OsdagBridge LaTeX report."""

PAGE_MARGIN = "22mm"
HEADER_HEIGHT = "15pt"
HEADER_SEPARATION = "8mm"
FOOTER_SEPARATION = "10mm"
TABLE_COLUMN_PADDING_PT = 5
COMPACT_TABLE_COLUMN_PADDING_PT = 3.5
DESIGN_TABLE_COLUMN_PADDING_PT = 4
ANALYSIS_TABLE_COLUMN_PADDING_PT = 3
TABLE_ROW_STRETCH = 1.12
ANALYSIS_TABLE_ROW_STRETCH = 1.25
TABLE_EXTRA_ROW_HEIGHT_PT = 0.6
LONGTABLE_PRE_SKIP = "0pt"
LONGTABLE_POST_SKIP = "6pt"
RULE_WIDTH_PT = 0.5

BRAND_GREEN_HEX = "91B014"
CHART_PASS_HEX = "5B8E3B"
CHART_FAIL_HEX = "C4473A"
CHART_NEUTRAL_HEX = "8091A5"
CHART_TEXT_HEX = "263238"
CHART_GRID_HEX = "DCE2E7"

UTILIZATION_FIGURE_WIDTH = r"0.92\textwidth"
MATERIAL_FIGURE_WIDTH = r"0.92\textwidth"
CHART_FIGURE_SIZE_INCH = (8.4, 3.7)
MATERIAL_CHART_SIZE_INCH = (8.4, 3.7)
FIGURE_DPI = 180


def latex_layout_preamble() -> str:
    """Return the global LaTeX layout declarations used by every chapter."""
    return rf"""
\usepackage[a4paper,margin={PAGE_MARGIN},headheight={HEADER_HEIGHT},headsep={HEADER_SEPARATION},footskip={FOOTER_SEPARATION}]{{geometry}}
\setlength{{\tabcolsep}}{{{TABLE_COLUMN_PADDING_PT}pt}}
\renewcommand{{\arraystretch}}{{{TABLE_ROW_STRETCH}}}
\setlength{{\LTpre}}{{{LONGTABLE_PRE_SKIP}}}
\setlength{{\LTpost}}{{{LONGTABLE_POST_SKIP}}}
\setlength{{\arrayrulewidth}}{{{RULE_WIDTH_PT}pt}}
\setlength{{\extrarowheight}}{{{TABLE_EXTRA_ROW_HEIGHT_PT}pt}}
\definecolor{{osdagGreen}}{{HTML}}{{{BRAND_GREEN_HEX}}}
"""
