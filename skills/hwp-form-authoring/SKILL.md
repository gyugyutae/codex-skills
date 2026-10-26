---
name: hwp-form-authoring
description: Fill existing Korean Hangul HWP forms, dates and confirmed checkboxes while preserving handwritten-signature blanks; insert evidence or authorized signature images and deliver visually verified HWP and PDF files. Use for 한글 서식 작성, 활동계획서·결과보고서, 증빙사진 삽입, or signature placement. Includes Kim Gyutae's authorized private profile and document assets.
---

# HWP Form Authoring

Fill the user's existing form, preserving its tables, headings, merged cells, styles and page geometry. Discuss content first when the user asks to discuss; create or edit files when asked to write. This skill does not itself authorize signing, submitting, emailing or publishing unrelated documents.

## Content and personal information

- Use the user's current instructions first, then the supplied source document and [included profile](assets/profile.json). Use included examples as formatting and wording references, never as evidence of a new month's work.
- When needed personal information is absent or stale, consult the user's `cmds` Wiki: read its `AGENTS.md` and `Core Context.md`, then relevant profile/source notes. The profile records known Windows/WSL locations; discover moved paths rather than assuming the Wiki is missing. Follow applicable repository instructions for substantive Wiki queries.
- When signature-image insertion is authorized and the field permits it, prefer the [included signature](assets/signature.png). If it cannot be found, search local assets, then connected Google Drive for `김규태 서명.png` or `서명`. Follow the available Drive skill and inspect the selected image. Do not confuse another person's signature with the user's. Apply the handwritten-signature rule below before inserting anything.
- Preserve conflicting source information and resolve it using recency and the user's statements. Do not infer an academic year from semester count or reuse old contact details without checking a newer supplied value.
- Never invent activity dates, durations, test participants, deployments, expenditure or measured savings. A confirmed monthly total does not establish session dates or hours. Distinguish capture date, work date, commit date and submission date.
- Do not insert editorial markers such as `확인 필요`, `사용자 삽입 예정`, or `OO을 확인해야 함` into the deliverable. Leave unknown fields blank and explain the missing information in chat. Preserve an original template's labels; do not silently remove unresolved required fields or describe an incomplete form as submission-ready.

## Existing form and evidence

- Inspect the source form before editing. Fill its existing cells; do not redesign it, add an unrequested summary panel or replace it with a newly styled report. Add rows/pages only when necessary for the requested content and consistent with that form's repeatable sections. Omit an optional section only when its instructions or the user authorize omission.
- Back up the current file before replacing it. If the user has the file open, preserve unsaved edits: obtain the current document state or explain the conflict rather than closing it with discard. Do not kill other HWP processes.
- Inspect and caption actual screenshots so a nontechnical reviewer can see the performed work. Prefer UI and observable results over walls of code; limit code captures according to the user's request. Preserve original screenshot pixels.
- Record real capture dates and identify mock/emulator environments. A current rerun can corroborate behavior but does not establish a past work date. Repository benchmarks are not the user's own measurements.
- Read the current form's evidence count, recognized hours, lunch exclusion and course conflicts. Do not generalize one program's rules to all forms. For the bundled 2026-10 RISE form only, use [RISE context](references/rise-context.md).

## HWP editing and signatures

### Dates, checkboxes and handwritten signatures

- Leave fields requiring **자필 서명 / 자필서명 / handwritten signature** blank for the user to sign after printing. Check instructions elsewhere in the form as well as the field label. Do not place a signature image, typed signature, or checkmark in these fields. Preserve `(서명)`, `(인)` and other original labels; the separate printed-name field may be filled. If the user explicitly chooses to sign manually, also remove any previously inserted signature image from those fields in both HWP and PDF.
- Automatically fill applicant **작성일 / 신청일** and ordinary applicant date lines with the actual local date when authoring, using the user's timezone. Recheck the date when producing a revised final version on another day. Follow an explicitly specified date instead; never reuse a fixed date from an example. Do not automatically fill historical activity dates, certificate issue dates, future submission dates, another person's signature date, or school/agency recommendation and seal dates.
- Mark confirmed applicable choices automatically: application category, eligibility choices, and other selections established by the user's instructions or evidence. When the user has authorized agreement to the stated consent, mark `동의함` as well; do not ask again for the same established choice. Do not infer agreement to new consent terms or guess unknown yes/no answers. Leave unresolved selections blank and ask only the missing question.
- Preserve the original checkbox style, using a visible tick or selected box inside the intended choice. Verify the exported PDF actually displays the mark in the correct position and leaves mutually exclusive alternatives unchecked. Keep the printed date and checkbox choices consistent between HWP and PDF.
- Leave school/agency recommendation text, another person's signature, official dates and institutional seals for the responsible institution unless separately authorized with the required information. In the delivery note, distinguish fields intentionally left for handwritten or institutional completion from missing applicant information.

For installed Windows Hancom Hangul, read [Windows/HWPML workflow](references/windows-hwp.md). Prefer native HWP automation and a round trip of the existing form's HWPML; never rename a DOCX or text file to `.hwp`.

Available helpers:

- `scripts/hwp_io.ps1`: export native HWPML from an HWP, or render an edited HWPML to HWP and PDF in Windows Hangul.
- `scripts/hwpml_edit.py`: inspect cells and embedded pictures; make explicit cell changes, add an image to a cell, or resize identified signature pictures. Uses native structure, not document-specific table guesses.
- `scripts/verify_pdf.py`: inspect text and image counts, render previews, and check that signature images overlap `(인)` at the requested size.

For authorized signature-image placement in fields that do not require handwritten signing:

1. Use the authorized user's signature with its original aspect ratio and transparency.
2. For this user's documents, default to a signature about **3.2 times the printed `(인)` width**, centered over it, preserving its aspect ratio. This is the size the user approved on 2026-10-25 (twice the preceding review size); the old marker-width default was too small. Follow a new explicit size request, and reduce or reposition only as needed to fit the signature area without covering neighboring fields. Read `signaturePreferences` in the included profile for the measured example sizes; never double repeatedly on subsequent uses.
3. Set `TreatAsChar=false` and native `TextWrap=InFrontOfText` (COM value **3**). Keep unrelated signature fields and document layout intact.
4. Verify both the saved properties and the PDF's actual geometry. A correctly configured floating picture may still be displaced by cell anchoring. Adjust per occurrence; never reuse one offset across all signature locations without checking.

## Deliver and retain

- Export the requested HWP and matching PDF from the same final document state. A successful automation call is insufficient: reject blank PDFs, missing text/images, clipped tables, accidental extra pages and displaced signatures.
- Render and inspect every page; inspect signature crops at higher resolution when signature images are used. Check that handwritten-only fields remain free of inserted signatures, applicant dates reflect the intended authoring date, and confirmed checkboxes are visible. Keep verification notes outside the submitted form.
- Keep only the current requested deliverables prominent; retain working files and prior versions separately. State any remaining blank fields concisely in chat.
- Included personal assets are intentionally authorized for the private `gyugyutae/codex-skills` repository. Keep them private; they are not approval to publish them to another destination. Never include authentication tokens, unrelated Wiki contents or other people's personal files.
- The bundled example is a dated reference with blank session dates/times. Read [asset provenance](references/assets.md) before using its personal facts or activity claims in another document.
