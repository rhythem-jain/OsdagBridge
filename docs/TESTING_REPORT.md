# Testing report

## Automated checks run

| Check | Method | Result |
|---|---|---|
| Python syntax | Python 3.12 compileall over report modules and the new unit module | Passed |
| Repeated LongTable headings | unittest with a minimal assembled LaTeX table | Passed; inserted continuation blocks and remained idempotent |
| UR extraction | unittest with synthetic unit-test results, non-finite input, and missing components | Passed; invalid and absent values remained unavailable |
| Chapter 3 table separation | unittest with a selected Class A vehicle and user footway input | Passed; separate tables and values were present |
| Chapter 7 figure placement | unittest checks the generated LaTeX after the bill of materials | Passed; chart path follows the table |
| Chart rendering | unittest with representative unit-test values and missing components in EB_2063 | Passed; both outputs were valid PNG files |
| LaTeX compilation | Tectonic CLI and the desktop compile tool | Blocked before TeX processing; package bundle was not cached and network access was unavailable |

The UR and quantity chart tests use synthetic values solely as isolated unit
fixtures. They are not OsdagBridge analysis results and are not evidence of an
integration run.

All five report-generator unit test methods passed in the available EB_2063
environment. The application-level checks below remain unverified.

## Not verified

- The available EB_2063 environment has Python 3.10.21, outside the project's
  declared Python 3.11–3.12 range. It contains Matplotlib and PySide6 but does
  not contain PyLaTeX, pytest, or pdflatex. A Tectonic executable is available,
  but its TeX resource bundle is missing and cannot be downloaded here.
- System Python 3.12 can compile the source but lacks Matplotlib, PyLaTeX,
  pytest, and PySide6.
- No compatible report environment or PDF compiler was available. The desktop
  analysis and report workflow was not run.
- No real design input or baseline report was supplied. No before/after PDF
  was generated and no page-level visual review was performed.

## Next integration checks

Use a Python 3.11 or 3.12 OsdagBridge environment with the project
dependencies, PyLaTeX if required by the runtime, and a working pdflatex. Run a
complete bridge design through the GUI, generate a report, then inspect page
breaks, headers, the footer region, Chapter 3, Section 5.5, and Chapter 7 in a
rendered PDF. Confirm the results against the GUI-selected vehicle and the
source result dictionaries.
