# Documents and account-aware draft creation

## Select and prepare

Read the official call and make a short checklist: label, required/recommended, exact file, why needed, status. Find files in the user's authorized workspace, existing application outputs and private document assets. Verify applicant, issue date/validity, legibility, final version and the notice's allowed format/page/size requirements. Inspect the actual file when duplicates or misleading names could select the wrong person/version. Ask if different valid bank accounts remain ambiguous; do not infer an account from a filename.

Automatically select the applicable mandatory files and useful optional files the user requested. Respect calls that forbid extra attachments. Recommendation letters/certificates must be genuine; drafting a request or filling an authorized form is different from issuing a certificate or signing for someone. Follow any existing form-authoring skill for HWP/signature constraints. Never fabricate missing official documents.

Examples:
- Scholarship application: completed original form and bank copy if requested, enrollment/transcript and eligibility evidence per notice; relevant statement/portfolio only if allowed.
- Developer internship: CV and relevant portfolio link/PDF, motivation if requested/useful; transcript/recommendation per call. Bank copy is normally irrelevant.
- First eligibility inquiry: concise questions; attach CV only if it helps and the recipient accepts files. Do not collect every available private document.

## Input and helper

Store input and output **outside the Git repository** in a private directory. Paths are resolved relative to the input JSON. Text must be UTF-8. The helper validates availability, nonempty files and an estimated encoded payload size; it does not certify document content or enforce every provider's limit.

```json
{
  "account": "student@example.edu",
  "to": "scholarships@example.org",
  "subject": "Scholarship application",
  "body": "Dear Scholarship Office,\nPlease find my application attached.",
  "attachments": [
    {"path": "application.pdf", "purpose": "required", "label": "신청서"},
    {"path": "bank.pdf", "purpose": "required", "label": "통장사본"},
    {"path": "cv.pdf", "purpose": "recommended", "label": "이력서"}
  ]
}
```

`compose` returns URL plus manifest, with `pending-upload` if files are selected. It never adds fake attachment URL parameters. `draft` requires `--output`; it writes connector arguments containing base64url attachment bytes with private permissions, not to stdout. The configurable default estimated payload ceiling is 20 MiB; actual provider/tool limits may be smaller. Missing recommended documents are reported; missing required files cause failure. To offer a text-only link despite missing mandatory files, preserve the original missing-document checklist separately and generate a separate text-only input without attachments; label the result incomplete, never silently downgrade required files to optional.

Each attachment may specify `filename`, e.g. `"filename": "GYUTAE_KIM_CV.pdf"`, to set a clean recipient-facing name without modifying the original. Use only a basename with its real extension. Duplicate names and extension changes are rejected. For UI uploads, make renamed private copies instead. See [business-mail.md](business-mail.md) for naming and correspondence defaults.

For an existing conversation, follow [replies.md](replies.md). Add `"reply_message_id": "<fetched Gmail message ID>"` to the input and use draft mode. A compose link cannot preserve verified reply context.

## Connector or browser

Discover current Gmail profile/create-draft/read-draft capabilities. Verify the account identity equals `account` before mutation. For the Gmail connector that accepts a MIME tree, `draftArgs` contains `to`, `subject` and a `multipart/mixed` payload: HTML-escaped text part followed by attachment parts with filename, MIME type, disposition and `base64_url_content`. Confirm the live schema before passing arguments. Never print the full payload to tool logs or expose it as a public URL. Retain private working files only as needed; remove temporary encoded payloads after verified upload without deleting source documents.

When the connector belongs to another account, switching a From field is not authentication. Use an authenticated browser's intended mailbox if available; upload selected local files using supported browser tools. Wait for upload completion, inspect file chips/count and sender, and capture the real draft URL. If a browser upload requires local path bridging unavailable in that environment, report that limitation; do not claim success.

Prefer an existing draft for retries rather than creating duplicates. Verify all files against the manifest after upload; if the tool only exposes metadata, state that verification scope. User-facing output: direct draft link, sender, required/recommended attachment names, remaining gaps. If no real draft link can be obtained, state that and offer the account's Drafts folder or a compose fallback with its distinct pending-attachment status; never present the fallback as the uploaded draft. Do not auto-send based on authorization to prepare or upload.
