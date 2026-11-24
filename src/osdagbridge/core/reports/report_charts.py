"""Data extraction and plotting helpers for report summary figures."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from .styles import (
    CHART_FAIL_HEX,
    CHART_GRID_HEX,
    CHART_NEUTRAL_HEX,
    CHART_PASS_HEX,
    CHART_TEXT_HEX,
    CHART_FIGURE_SIZE_INCH,
    MATERIAL_CHART_SIZE_INCH,
    FIGURE_DPI,
)


def _color(value: str) -> str:
    return value if value.startswith("#") else f"#{value}"


def _finite_number(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _max_finite(values) -> float | None:
    valid = [number for value in values if (number := _finite_number(value)) is not None]
    return max(valid) if valid else None


def _nested_efficiencies(value: Any):
    """Yield actual efficiency/UR values from nested component result mappings."""
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() in {"efficiency", "utilization_ratio", "ur", "dcr"}:
                number = _finite_number(child)
                if number is not None:
                    yield number
            else:
                yield from _nested_efficiencies(child)
    elif isinstance(value, (list, tuple)):
        for child in value:
            yield from _nested_efficiencies(child)


def utilization_summary(output_dict: dict) -> dict[str, float | None]:
    """Return the controlling reported UR for each primary element, when present.

    No missing or invalid result is converted into a numerical zero.
    """
    output_dict = output_dict or {}
    girder_checks = (
        (output_dict.get("design_results") or {}).get("per_girder") or {}
    )
    girder_values = []
    for girder in girder_checks.values():
        if not isinstance(girder, dict):
            continue
        for check in (girder.get("checks") or []):
            if isinstance(check, dict):
                girder_values.append(check.get("dcr"))
        for load_case, result in (girder.get("per_lc") or {}).items():
            if str(load_case).lower().startswith("envelope") or not isinstance(result, dict):
                continue
            for check in (result.get("checks") or []):
                if isinstance(check, dict):
                    girder_values.append(check.get("dcr"))

    # Deck URs are calculated from the same demand/capacity results as Table 5.22.
    deck = output_dict.get("deck_report_values") or {}
    from osdagbridge.core.utils.common import (
        KEY_DD_M_ULS_HOG, KEY_DD_M_ULS_OH, KEY_DD_M_ULS_SAG,
        KEY_DD_MU_BOT, KEY_DD_MU_OH, KEY_DD_MU_TOP,
        KEY_DD_PUNCH_VED, KEY_DD_VRD_C_MPA,
        KEY_DD_SHEAR_VED, KEY_DD_SHEAR_VRDC,
        KEY_DD_WK_BOT, KEY_DD_WK_LIMIT, KEY_DD_WK_OH, KEY_DD_WK_TOP,
    )
    deck_ratios = []
    for demand_key, capacity_key in (
        (KEY_DD_M_ULS_SAG, KEY_DD_MU_BOT),
        (KEY_DD_M_ULS_HOG, KEY_DD_MU_TOP),
        (KEY_DD_M_ULS_OH, KEY_DD_MU_OH),
        (KEY_DD_PUNCH_VED, KEY_DD_VRD_C_MPA),
        (KEY_DD_SHEAR_VED, KEY_DD_SHEAR_VRDC),
    ):
        demand, capacity = _finite_number(deck.get(demand_key)), _finite_number(deck.get(capacity_key))
        if demand is not None and capacity is not None and capacity > 0:
            deck_ratios.append(demand / capacity)
    crack_limit = _finite_number(deck.get(KEY_DD_WK_LIMIT))
    if crack_limit is not None and crack_limit > 0:
        for key in (KEY_DD_WK_BOT, KEY_DD_WK_TOP, KEY_DD_WK_OH):
            width = _finite_number(deck.get(key))
            if width is not None:
                deck_ratios.append(width / crack_limit)

    cb_results = output_dict.get("crossbracing_design_results")
    if cb_results is None:
        cb_results = output_dict.get("crossbracing_forces_dict")
    ed_results = output_dict.get("end_diaphragm_design_results")
    if ed_results is None:
        ed_results = output_dict.get("enddiaphragm_design_results")

    return {
        "Steel plate girders": _max_finite(girder_values),
        "Concrete deck slab": _max_finite(deck_ratios),
        "Cross bracing": _max_finite(_nested_efficiencies(cb_results)),
        "End diaphragms": _max_finite(_nested_efficiencies(ed_results)),
    }


def _plot_modules():
    import matplotlib
    matplotlib.use("Agg", force=True)
    import matplotlib.pyplot as plt
    return plt


def create_utilization_chart(summary: dict[str, float | None], path: str | Path) -> str:
    """Write the UR summary chart, marking missing component checks explicitly."""
    plt = _plot_modules()
    labels = list(summary)
    values = [summary[label] for label in labels]
    plotted = [value if value is not None else 0.0 for value in values]
    colors = [
        _color(CHART_NEUTRAL_HEX) if value is None else
        (_color(CHART_FAIL_HEX) if value > 1.0 else _color(CHART_PASS_HEX))
        for value in values
    ]
    fig, ax = plt.subplots(figsize=CHART_FIGURE_SIZE_INCH, constrained_layout=True)
    bars = ax.bar(range(len(labels)), plotted, color=colors, width=0.62)
    ax.axhline(1.0, color=_color(CHART_FAIL_HEX), linestyle="--", linewidth=1.5,
               label="Limit (UR = 1.0)")
    ax.set_ylabel("Utilization Ratio")
    ax.set_xticks(range(len(labels)), labels, rotation=12, ha="right")
    ax.set_ylim(bottom=0, top=max(1.15, max((v for v in plotted), default=0) * 1.18))
    ax.grid(axis="y", color=_color(CHART_GRID_HEX), linewidth=0.7, alpha=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(colors=_color(CHART_TEXT_HEX))
    ax.spines[["top", "right"]].set_visible(False)
    for bar, value in zip(bars, values):
        label = "N/A" if value is None else f"{value:.2f}"
        ax.annotate(label, (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    xytext=(0, 4), textcoords="offset points",
                    ha="center", va="bottom", fontsize=8, color=_color(CHART_TEXT_HEX))
    ax.legend(frameon=False, loc="upper right")
    fig.savefig(path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)
    return str(path)


def _quantity(value: Any) -> float | None:
    if value in (None, "", "N.A.", "N/A", "---"):
        return None
    return _finite_number(value)


def _sum_quantities(quantities: dict, keys: tuple[str, ...]) -> float | None:
    values = [_quantity(quantities.get(key)) for key in keys]
    if not values or any(value is None for value in values):
        return None
    return sum(values)


def create_material_quantity_chart(quantities: dict, path: str | Path) -> str:
    """Write steel tonnage and concrete/reinforcement quantity charts."""
    plt = _plot_modules()
    steel = {
        "Girders": _quantity(quantities.get("steel_girders_wt_total")),
        "Cross bracing": _sum_quantities(quantities, (
            "bracing_top_wt_total", "bracing_bot_wt_total", "bracing_diag_wt_total",
        )),
        # End-diaphragm take-off is not currently emitted by the BOQ generator.
        "End diaphragms": None,
    }
    civil = (
        ("Concrete deck", _quantity(quantities.get("concrete_deck_vol_total")), "m³"),
        ("Reinforcement", _quantity(quantities.get("rebar_deck_wt_total")), "MT"),
    )
    fig, axes = plt.subplots(1, 3, figsize=MATERIAL_CHART_SIZE_INCH, constrained_layout=True)
    panels = [
        (axes[0], "Structural steel", "Weight (MT)", list(steel.items())),
        (axes[1], "Concrete deck", "Volume (m³)", [(civil[0][0], civil[0][1])]),
        (axes[2], "Reinforcement", "Weight (MT)", [(civil[1][0], civil[1][1])]),
    ]
    for axis, title, unit, entries in panels:
        labels = [entry[0] for entry in entries]
        values = [entry[1] for entry in entries]
        bars = axis.bar(
            range(len(labels)),
            [value or 0 for value in values],
            color=[_color(CHART_NEUTRAL_HEX if value is None else CHART_PASS_HEX)
                   for value in values],
            width=0.62,
        )
        axis.set_title(title)
        axis.set_ylabel(unit)
        axis.set_xticks(range(len(labels)), labels, rotation=12, ha="right")
        for bar, value in zip(bars, values):
            axis.annotate(
                "N/A" if value is None else f"{value:.2f}",
                (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8,
            )
        axis.grid(axis="y", color=_color(CHART_GRID_HEX), linewidth=0.7, alpha=0.8)
        axis.set_axisbelow(True)
        axis.spines[["top", "right"]].set_visible(False)
    fig.savefig(path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)
    return str(path)
