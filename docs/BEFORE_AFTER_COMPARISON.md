# Before/after comparison and requirement audit

No Report_Before.pdf or design input was present, and the available Python
environment has no pdflatex. This document compares the inspected source
behavior with the code changes; it does not claim a PDF comparison.

| Issue | Original source behavior | Modified source behavior | Evidence |
|---|---|---|---|
| Continued table headings | LongTable blocks generally had no continuation heading declarations. | The assembled TeX receives first-page and continued-page heading blocks when a bold header row can be identified. | repeat_longtable_headers() in core/reports/report_generator.py; unit test passed. |
| Footer and page layout | Geometry and table spacing were inline in the report preamble; PDF overlap could not be inspected. | Page and table layout values now come from core/reports/styles.py; needspace guard remains. | Source inspection only; needs a compiled PDF visual check. |
| Chapter 3 vehicle/footway loads | One table combined the selected vehicles, impact, braking, and footway pressure. | Separate vehicle and footway tables read their data from the report input dictionary. Unsupported centrifugal-force data is identified as unavailable. | core/reports/chap3.py; selected vehicle unit test passed. |
| Chapter 5 utilization chart | Numerical overall design summary only. | UR chart is generated from finite existing result values, has a red dashed UR=1.0 line, and labels missing data as N/A. | core/reports/report_charts.py and report_generator.py; mock-data chart test passed. |
| Chapter 7 quantity chart | Numerical bill of materials only. | Chart is generated from calculated Chapter 7 quantities and shows steel, concrete, and reinforcement in separate units. End diaphragm quantity is N/A because the BOQ does not currently provide it. | core/reports/report_charts.py; mock-data chart test passed. |
| Centralized styling | Shared layout values were inline in report_generator.py; chapter-level local column widths remain. | Global page/table/chart settings and chapter-specific padding values are in core/reports/styles.py and are consumed by the orchestrator, chapters, and chart utilities. | Source inspection; table column widths remain local to each table. |

## Requirement status

| Requirement | Status | Reason |
|---|---|---|
| 1. Repeated table headers | Partially verified | Source transform and unit test passed; continuation pages were not rendered. |
| 2. Footer and layout fixes | Partially verified | Shared geometry and spacing configuration added; no PDF was available to inspect. |
| 3. Load and geometry tables | Partially verified | Vehicle and footway tables are separate and dynamically sourced. Centrifugal force is not present in report data. |
| 4. Utilization ratio charts | Partially verified | Dynamic chart wiring and isolated tests are in place; no actual design analysis or PDF was run. |
| 5. Material quantity charts | Partially verified | Dynamic charts use existing Chapter 7 outputs; end-diaphragm quantities are unavailable in the existing BOQ. |
| 6. Centralized style system | Partially verified | Shared module supplies global layout/chart settings and chapter-specific table padding; column widths remain table-specific. |

## Integration evidence still needed

Generate the baseline and modified PDFs from the application using the same
bridge inputs. Record page counts and inspect all longtable continuations,
footer clearance, Chapter 3 tables, Section 5.5, and Chapter 7. Do not mark
these integration items verified until that evidence exists.
