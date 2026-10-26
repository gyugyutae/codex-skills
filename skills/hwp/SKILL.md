---
name: hwp
description: Fill or revise existing Korean HWP forms, applicant dates, confirmed checkboxes and evidence; preserve handwritten-signature blanks and verify HWP/PDF output. Use for 한글 서식 작성, 활동계획서·결과보고서, 증빙 삽입 or authorized signature-image placement. Includes private Kim Gyutae assets.
---

# HWP Form Authoring

Fill the existing form and deliver matching, visually checked HWP and PDF files.
Preserve tables, headings, merged cells, styles and page geometry.

## Choose the task

| Request | Action |
| --- | --- |
| Discuss content | Inspect and discuss; do not write yet. |
| Fill/revise HWP | Read [Windows/HWPML workflow](references/windows-hwp.md); export, edit selected cells, render. |
| Personal information/evidence | Read [content rules](references/content-rules.md); prefer current instructions over dated assets. |
| Dates/choices/signatures | Apply field rules below; read [signature placement](references/signatures.md) only for authorized images. |

## Fill fields

- **Dates:** use the actual authoring date in the user's timezone for applicant 작성일/신청일;
  recheck on later revisions. Follow explicit dates instead. Do not guess historical/future
  dates or fill school/agency date lines.
- **Choices:** check established applicable choices and user-authorized consent. Do not
  re-ask settled choices, guess unresolved answers or infer new consent.
- **Handwritten signatures:** inspect instructions throughout the form; leave 자필서명 fields
  blank and preserve labels. Type separate name fields. Remove earlier image signatures
  from both outputs when manual signing is requested.
- **Institution fields:** leave recommendation text, others' signatures, official dates
  and seals to the institution unless separately authorized with the required information.
- Leave unknown values blank; ask only blocking questions. No editorial placeholders
  inside the form. Do not infer activity facts from examples.

## Edit and render

Back up replaced files, preserve unsaved work and never kill unrelated HWP processes.
Fill existing cells without redesigning the form. Add repeatable rows/pages only when
needed; omit sections only when the form or user authorizes it.

```powershell
.\scripts\hwp_io.ps1 -Mode Export -InputPath C:\work\source.hwp -OutputPath C:\work\source.xml
```

```sh
python scripts/hwpml_edit.py source.xml
python scripts/hwpml_edit.py source.xml --manifest edits.json --output edited.hml
```

```powershell
.\scripts\hwp_io.ps1 -Mode Render -InputPath C:\work\edited.hml -OutputPath C:\work\staging\result.hwp
```

Commands require Windows Hangul COM automation; see the linked workflow for environment
requirements and recovery. Never rename another file format to .hwp.

## Verify and deliver

```sh
python scripts/verify_pdf.py result.pdf --require 'Required text' --render-dir previews
# Image signatures: verify saved native properties and rendered placement.
python scripts/verify_pdf.py result.pdf --roundtrip result.roundtrip.xml --expected-signatures 2
# Handwritten field: page number is 1-based; reject images over this marker.
python scripts/verify_pdf.py result.pdf --blank-signature '3:(서명)'
```

Default markers: `(인)`, `(서명)`, `(인 또는 서명)`. Repeated `--signature-marker`
options select other labels; see [verification limits](references/signatures.md).
Inspect every page and high-resolution signature crops. Reject blank pages, missing/clipped
content, displaced signatures or invisible checks; verify dates and handwritten blanks.
Deliver current HWP/PDF with working files separate; state remaining user/institution work.
This skill does not authorize submission, unrelated signing, emailing or publishing.
