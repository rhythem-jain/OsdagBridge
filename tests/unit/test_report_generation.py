"""Focused unit checks for report layout, extraction, and chart helpers."""

import tempfile
import unittest
from pathlib import Path

from osdagbridge.core.reports.report_charts import (
    create_material_quantity_chart,
    create_utilization_chart,
    utilization_summary,
)
from osdagbridge.core.reports.report_generator import repeat_longtable_headers
from osdagbridge.core.reports.chap3 import ch3_loads
from osdagbridge.core.reports.chap7 import ch7_quantities
from osdagbridge.core.utils.common import (
    KEY_LL_IRC_CLASS_A,
    KEY_LL_IRC_70R_TRACKED,
    KEY_LL_FOOTPATH_PRESSURE_MODE,
    KEY_LL_FOOTPATH_PRESSURE_VALUE,
    KEY_DD_M_ULS_SAG,
    KEY_DD_MU_BOT,
)


class ReportGenerationTests(unittest.TestCase):
    def test_longtable_header_is_repeated_and_idempotent(self):
        tex = (
            r"\begin{longtable}{|c|c|}" "\n"
            r"\caption{Example}" "\n"
            r"\hline" "\n"
            r"\textbf{A} & \textbf{B} \\" "\n"
            r"\hline" "\n"
            r"one & two \\" "\n"
            r"\end{longtable}"
        )
        output = repeat_longtable_headers(tex)
        self.assertIn(r"\endfirsthead", output)
        self.assertIn(r"\endhead", output)
        self.assertEqual(output, repeat_longtable_headers(output))

    def test_utilization_extraction_uses_finite_results_and_keeps_missing(self):
        output = {
            "design_results": {
                "per_girder": {
                    "G1": {"checks": [{"dcr": 0.72}, {"dcr": float("nan")}]},
                    "G2": {"checks": [{"dcr": 1.08}]},
                }
            },
            "crossbracing_design_results": {
                "G1-G2": {
                    "diagonal": {"compression": {"Member.efficiency": 0.43}},
                    "chord": {"tension": {"Optimum.UR": 0.38}},
                }
            },
            "end_diaphragm_design_results": {
                "G1-G2": {
                    "diagonal": {"compression": {"Member.efficiency": 0.30}},
                    "chord": {"tension": {"Optimum.UR": 0.28}},
                }
            },
            "deck_report_values": {
                KEY_DD_M_ULS_SAG: 10.0,
                KEY_DD_MU_BOT: 0.0,
            },
        }
        summary = utilization_summary(output)
        self.assertEqual(summary["Steel plate girders"], 1.08)
        self.assertEqual(summary["Cross bracing"], 0.43)
        self.assertEqual(summary["End diaphragms"], 0.30)
        self.assertIsNone(summary["Concrete deck slab"])

    def test_load_report_separates_selected_vehicle_from_footway(self):
        tex = ch3_loads({
            KEY_LL_IRC_CLASS_A: True,
            KEY_LL_IRC_70R_TRACKED: True,
            KEY_LL_FOOTPATH_PRESSURE_MODE: "User-defined",
            KEY_LL_FOOTPATH_PRESSURE_VALUE: "4.0",
        })
        self.assertIn("Vehicle Live Load Parameters", tex)
        self.assertIn("Class A", tex)
        self.assertIn("Class 70R (Tracked)", tex)
        self.assertIn("Footway Live Load Parameters", tex)
        self.assertIn("4.0", tex)
        assembled = repeat_longtable_headers(tex)
        self.assertEqual(
            assembled.count(r"\begin{longtable}"),
            assembled.count(r"\endhead"),
        )

    def test_material_chart_is_embedded_after_quantity_table(self):
        tex = ch7_quantities({}, material_chart_path="images/materials.png")
        self.assertIn(r"\includegraphics[width=0.92\textwidth]{images/materials.png}", tex)
        self.assertLess(tex.index(r"\end{longtable}"), tex.index(r"\includegraphics"))

    def test_chart_writers_create_png_files_with_missing_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            utilization_path = Path(tmp) / "ur.png"
            material_path = Path(tmp) / "materials.png"
            create_utilization_chart(
                {
                    "Steel plate girders": 1.12,
                    "Concrete deck slab": 1.0,
                    "Cross bracing": None,
                    "End diaphragms": None,
                },
                utilization_path,
            )
            create_material_quantity_chart(
                {
                    "steel_girders_wt_total": "12.4",
                    "bracing_top_wt_total": "1.2",
                    "bracing_bot_wt_total": "0",
                    "bracing_diag_wt_total": "2.0",
                    "concrete_deck_vol_total": "24.0",
                    "rebar_deck_wt_total": "0",
                },
                material_path,
            )
            self.assertTrue(utilization_path.is_file())
            self.assertTrue(material_path.is_file())
            self.assertEqual(utilization_path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(material_path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")


if __name__ == "__main__":
    unittest.main()
