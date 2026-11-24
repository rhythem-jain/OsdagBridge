# Existing report architecture

## Generation path

The desktop output dock opens the report options dialog through
desktop/ui/template_page.py. The report worker calls
PlateGirderBridge.generate_design_report() in
core/bridge_types/plate_girder/plategirderbridge.py, which snapshots the
input and output dictionaries and builds a ReportPayload.

core/reports/report_generator.py is the report orchestrator. It copies
figures and logos into a temporary directory, calculates the Chapter 7 material
take-off through core/boq/boq_generator.py, calls the executive summary and
chapter functions, writes a .tex file, invokes pdflatex twice, and copies the
resulting PDF and TeX source to the requested output directory. The temporary
image directory is removed when compilation finishes.

The chapter content is split across executive_summary.py and chap1.py through
chap9.py. report_utils.py provides LaTeX escaping, common value rendering, and
figure embedding. Chapters 2 through 5 and 7 use LaTeX longtable; the current
report generator uses raw LaTeX templates rather than PyLaTeX objects.

## Data flow

- GUI inputs and computed output values reach build_report_payload() as
  dictionaries. Chapter 3 reads selected vehicle flags, custom vehicles,
  span, lane count, footway mode/value, and other load inputs from the input
  dictionary.
- Chapter 5 reads girder design results, deck report values, and transverse
  member results from the output dictionary through ReportDataBridge.
- Chapter 7 quantities are calculated from the input/output dictionaries by
  calculate_material_quantities() and then rendered by chap7.py.
- Report figures are captured by the bridge workflow and passed to chapter
  functions as paths or image bytes.

## Formatting before this change

The document preamble in report_generator.py owns package imports, page
geometry, table spacing, colors, and fancyhdr definitions. Chapter files also
contain local width and spacing values. Many tables use longtable, but most
did not declare a continuation header. Chapter 3 put vehicle live-load and
footway data in one table. Chapter 5 had a numerical overall design summary but
no UR chart. Chapter 7 had a bill of materials but no quantity chart.

## Constraints found in this checkout

The supplied folder has no Git metadata: .git exists as an empty directory.
There is no branch, commit hash, remote, or working-tree status to verify. The
available EB_2063 Conda environment uses Python 3.10.21, while environment.yml
requires Python 3.11 or 3.12. It has Matplotlib and PySide6, but no PyLaTeX,
pytest, or pdflatex. The system Python 3.12 has NumPy but not the report or GUI
dependencies. The GUI workflow and real before/after PDF generation therefore
could not be verified in this session.

No pre-existing baseline PDF or bridge design input was supplied. A baseline
PDF has not been synthesized.
