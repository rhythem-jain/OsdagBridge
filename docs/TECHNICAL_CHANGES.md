# Technical changes

## Report layout and style

- Added core/reports/styles.py as the shared source for page geometry, header
  and footer spacing, table padding/row spacing, brand colors, chart colors,
  chart dimensions, and figure widths.
- Updated the document preamble and chapter-level dense table settings to
  consume shared page, table padding, and row spacing values.
- Added repeat_longtable_headers() to report_generator.py. It works on the
  fully assembled TeX, identifies the bold heading row between the first two
  horizontal rules in each longtable, and emits endfirsthead/endhead blocks.
  Existing manually repeated headers are left alone.
- Kept the existing needspace guard for tables. PDF inspection is still needed
  to confirm the footer and long table behavior in the actual application.

## Chapter 3 loading tables

chap3.py now renders vehicle live loads and footway loads independently. The
vehicle table lists the vehicle selection from the UI and the available impact
and braking values. Footway mode and pressure come from the selected input
mode/value, including the code default when the mode requests it.

The current report data model does not expose centrifugal force values to this
chapter. The table states that plainly instead of supplying a guessed value.
The selected vehicle is dynamically mapped; it is not hardcoded.

## Summary charts

report_charts.py extracts finite URs from existing design outputs and creates
PNG figures using Matplotlib's non-interactive Agg backend. The UR plot uses
actual girder DCRs, deck demand/capacity values, and transverse-member
efficiencies. It draws a red dashed UR=1.0 line, colors passing and failing
bars differently, and labels missing component results as N/A.

The material chart reads the quantities already produced by
calculate_material_quantities(). It separates steel tonnage, concrete volume,
and reinforcement tonnage into panels with their own units. The current BOQ
does not emit an end-diaphragm quantity, so that chart entry is explicitly N/A.
Both generated images are stored under the report's temporary directory,
embedded from there, and removed after PDF generation.

The summary chart is inserted after the overall summary table in Chapter 5.
The material chart follows the numerical bill of materials in Chapter 7.

## Tests and implementation limits

tests/unit/test_report_generation.py covers repeated-header insertion,
idempotence, finite/missing utilization extraction, live-load table separation,
and PNG generation with missing values.

The current output dictionary does not supply centrifugal-force values, and
the current BOQ does not calculate end-diaphragm quantities. These gaps need
source data or an engineering-approved quantity method before those values can
be charted. No structural calculation logic was changed.
