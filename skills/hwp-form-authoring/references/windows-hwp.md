# Windows Hangul / HWPML workflow

## Runtime and preserving existing work

Windows Hancom Hangul with `HWPFrame.HwpObject` COM automation is required for the bundled PowerShell helper. PowerShell 5.1 script files containing Korean paths must be UTF-8 with BOM; otherwise file names become corrupt. Set console output to UTF-8. WSL may invoke `powershell.exe -NoProfile -ExecutionPolicy Bypass -File <Windows-path>`.

Use `Resolve-Path`, `Join-Path` and structured arguments. Do not interpolate private file contents into shell code. Do not print secrets. Keep a backup before overwriting. Export new files into a staging folder; verify them before replacing deliverables.

If a target is open, check for unsaved edits. A new COM object is safe for staging but does not include another window's unsaved work. Close/reopen only the relevant window when that can be done without discarding user changes. Never terminate all HWP processes to unlock a file.

## Export, edit, render

```powershell
.\hwp_io.ps1 -Mode Export -InputPath C:\work\source.hwp -OutputPath C:\work\source.xml
.\hwp_io.ps1 -Mode Render -InputPath C:\work\edited.hml -OutputPath C:\work\staging\report.hwp
```

`GetTextFile('HWPML2X','')` returns a .NET Unicode string whose XML declaration says UTF-16. When saving as UTF-8, change that declaration. When reading a saved UTF-8 export with an old declaration, parse Unicode text without the declaration or normalize it first.

Preserve `HEAD` style/ID tables, `BODY/SECTION` page definitions and `TAIL/BINDATASTORAGE`. Tables use zero-based `RowAddr`/`ColAddr`; merged cells may leave addresses absent. Verify the selected cell by reading its existing text. Do not flatten the whole document into text.

Inspect native addresses first, then apply a task-specific JSON manifest:

```sh
python hwpml_edit.py source.xml
python hwpml_edit.py source.xml --manifest edits.json --output edited.hml
```

Supported manifest sections (all optional):

```json
{
  "cells": [{"table": 1, "row": 0, "col": 1, "text": "Replacement text"}],
  "replacements": [{"old": "Exact existing text", "new": "", "expected_count": 1}],
  "resize_pictures": [{
    "comment_contains": "SIGNATURE_OVER_IN", "occurrence": 0,
    "width": 6400, "height": 2646, "signature": true,
    "position": {"HorzRelTo": "Paper", "VertRelTo": "Paper", "HorzAlign": "Left", "VertAlign": "Top", "HorzOffset": "49650", "VertOffset": "66560", "FlowWithText": "false"}
  }],
  "images": [{
    "table": 4, "row": 3, "col": 1, "file": "capture.png",
    "caption": "Actual observed behavior", "para_shape": "33",
    "max_width": 17000, "max_height": 28000
  }]
}
```

The addresses, style IDs, dimensions and offsets above illustrate the bundled case; inspect the new document before choosing them. Each image path is relative to the manifest unless absolute. Image insertion requires an existing native picture to clone. Cell replacement removes that cell's previous contents (including pictures); use only on the intended editable cell. Replacement counts fail closed on mismatches. Save to a new path.

For PDF verification:

```sh
python verify_pdf.py report.pdf --roundtrip report.roundtrip.xml \
  --require "Required text" --forbid "Unwanted editorial marker" \
  --expected-images 12 --expected-signatures 2 --render-dir previews
```

Image counts are per displayed occurrence, including signatures. Signature checks use the native `SIGNATURE_OVER_IN` picture comment by default; set `--signature-comment` to the actual marker used in another document. PDF geometry is a candidate check and still requires visual confirmation that the matched image is the intended signature.

Open edited XML with `Open(path, 'HWPML2X', 'forceopen:true')`. During this workflow, `SetTextFile` returned success but produced an empty document. Do not rely on that call without readback. Save HWP and PDF with `SaveAs`, then export a round-trip XML and inspect the actual PDF.

File access dialogs may require permission. `ALT+Y` means allow access and `ALT+N` means allow all for that automation instance; **ALT+A means deny**. Match the actual dialog and application instance. Do not press keys in unrelated windows or suppress unrelated errors. Use only installed/trusted security modules if one is already configured; do not download an arbitrary DLL to bypass prompts.

## Pictures and signatures

For COM insertion, `InsertPicture(path, true, 1, false, false, 0, width_mm, height_mm)` returns a picture control. On that control:

```powershell
$props = $picture.Properties
$props.SetItem('TreatAsChar', $false)
$props.SetItem('TextWrap', 3)
$picture.Properties = $props
```

The native round trip must show:

```xml
<SHAPEOBJECT TextWrap="InFrontOfText">
  <POSITION TreatAsChar="false" ... />
</SHAPEOBJECT>
```

COM's `TextWrap=3` is the Hancom automation enum. Other libraries may expose a different numbering scheme; do not substitute their numbers. [Hancom ParameterSetTable](https://raw.githubusercontent.com/hancom-io/devcenter-archive/main/hwp-automation/ParameterSetTable_2504.pdf) documents the automation values.

Native dimensions and offsets use HWPUNIT, normally 100 per point (about 283.46 per mm). Measure `(인)` in the PDF, use the user's approved width ratio from `assets/profile.json` (currently 3.2), preserve the image aspect ratio, then match its center to the marker center. The user rejected the old 1x-marker default as too small. Do not assume a page-wide or cell-wide reference frame; the approved example measures 6400×2646 and 5420×2240 HWPUNIT, with different marker widths.

Observed anchoring behavior:

- For `HorzAlign=Right`, a positive `HorzOffset` moved the image left. For `Center`, positive moved it right.
- `FlowWithText=true` in a cell clamped a negative vertical offset. Setting it false inside that cell moved the object outside its intended cell. A positive offset with the original cell anchor was more reliable.
- Resizing right-aligned images changes their center even if the offset stays constant. Recompute after resizing.
- When a cell anchor prevents vertical centering, a floating picture may instead use explicit `Paper` horizontal/vertical references and measured page coordinates. Measure the marker in that document and verify the round trip; do not copy the example's page offsets into another form.

These are observed cases, not universal coordinates. Inspect the exported PDF after each material correction. Check that any unrelated document geometry stays unchanged.

## Validation

`verify_pdf.py` requires PyMuPDF. The editor's image insertion needs Pillow; plain inspection/cell editing/resizing uses the Python standard library. Install dependencies in a task-local virtual environment when unavailable.

Check text and image count on every page, signature settings in round-trip HWPML, and actual image/marker intersections in the PDF. Render previews and inspect them visually; geometry checks alone cannot detect unreadable captions or the wrong photograph. Keep unresolved fields blank and report them in chat, not as editorial notes inside the form.
