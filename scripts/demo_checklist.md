# Report generator demonstration checklist

## Prepare a reproducible run

1. Use the official OsdagBridge development checkout with Python 3.11 or 3.12.
2. Install the environment from environment.yml and confirm that the GUI,
   report dependencies, and pdflatex are available.
3. Open the existing OsdagBridge desktop application.
4. Create a bridge design configuration and record its span, girder count,
   materials, deck dimensions, and selected vehicle from Additional Inputs >
   Loading.
5. Set a footway pressure mode and value, then save the input configuration.
6. Run Design to completion and preserve the analysis output.
7. Generate the original report from the same configuration before using the
   enhanced source, and save it as deliverables/Report_Before.pdf.
8. Switch to the enhanced source while preserving the same saved design input.
9. Run Design again and generate deliverables/Report_After.pdf.

## Inspect the enhanced report

- Confirm a table header repeats after at least one natural page break.
- Inspect pages that contain tables close to the footer and check for clipping.
- In Chapter 3, confirm vehicle and footway loads appear in distinct tables and
  the selected vehicle matches the loading tab.
- In Section 5.5, compare the UR bars with the design output values and verify
  the UR=1.0 threshold line.
- In Chapter 7, compare each plotted quantity with Table 7.1. Confirm any N/A
  values are genuinely absent from the BOQ output.
- Review the complete report for missing figures, malformed symbols, or
  overfull pages.
- Record PDF page count, software/environment versions, selected vehicle,
  report date, and any unavailable result fields.

## Capture truthful evidence

- Capture the live application and generated PDFs directly; do not substitute
  mockups for an application run.
- Keep screenshots of the source design inputs and relevant PDF pages with the
  submission materials.
- Do not claim the GUI, report compilation, or visual comparison passed until
  the steps above have been completed on a compatible environment.

The current workspace does not yet contain a baseline design input, generated
PDFs, or a compatible report-generation environment, so these integration steps
remain to be run.
