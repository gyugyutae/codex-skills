---
name: application-mail
description: Use when preparing scholarship, internship or other application emails with a direct Gmail compose link, required documents and relevant supporting attachments; also for 확인메일, 지원메일, 방문 요청 and 추천서 요청.
---

# Application mail

Deliver a clickable email action **directly in chat**, from the requested account, with truthful attachment status. Leave final sending to the user unless they explicitly request sending.

## Choose the task

| Need | Action |
| --- | --- |
| Text-only email | Generate a Gmail compose URL; put `[메일 작성하기](URL)` in chat, not behind an EML or Markdown file. |
| Email with documents | Prepare and upload attachments into an unsent draft using the correct account's connector or authenticated webmail. Return the verified draft link in chat. A compose URL cannot attach local files. |
| Formal application | Check the official submission channel. An inquiry email is not a portal application; do not substitute email where the employer/institution requires its form. |

## Run

1. Read the official notice, recipient, deadline and required documents. Reuse confirmed personal facts; for this user's defaults read [personal-defaults.md](references/personal-defaults.md). Apply the active workspace's application-writing rules. Ask only about a real unresolved choice, such as which bank account to use when multiple valid copies exist.
2. Find existing documents in authorized local sources before requesting them again. Classify required and recommended files. Prepare missing materials that can truthfully be authored (CV, motivation, portfolio); obtain official certificates and genuine recommendations from their issuers. Read [attachments.md](references/attachments.md) when any file is involved. For submission correspondence, apply [business-mail.md](references/business-mail.md): professional subject/body/signature and clear, automatically cleaned attachment names; preserve originals.
3. Build the message and manifest with the helper below. Use `compose` for a direct text link, or `draft` for connector-ready MIME attachments. Inspect metadata, not base64 file contents. The helper prepares data only; it never uploads or sends.
4. For attachments, verify the connector account identity first. Use its current schema to create the unsent draft and attach every selected file; alternatively use authenticated GNU webmail UI. Never use a personal connector and merely change `From` to impersonate GNU. Re-read the created draft/UI to verify recipients, actual sender account, attachment names/count and content/size where available. Do not guess a draft URL; use a returned or observed link. If an attachment upload fails, remove/repair incomplete drafts or mark them incomplete rather than ready.
5. Put the link in the chat, name the included files and identify any missing required files. If no correct-account upload capability is available, provide the compose link plus exact local file links and state automatic upload is incomplete. Do not describe a download bundle or MIME payload as an attached draft. Record status as prepared / user-reported sent / confirmed sent / portal submitted, with evidence scope.

```bash
python3 scripts/prepare_mail.py --input /absolute/private/mail.json --mode compose
python3 scripts/prepare_mail.py --input /absolute/private/mail.json --mode draft --output /absolute/private/draft-payload.json
```

Input schema and connector steps: [attachments.md](references/attachments.md). Keep account numbers, identity documents, certificates and generated payloads out of the skill repository. When publishing skill changes, read the **destination repository's** AGENTS.md/agent.md and scoped rules first; use its template, validation and Git workflow. Push only authorized changes, and verify the remote commit.

## Verify and deliver

- Round-trip the URL's account/recipient/subject/body, including Korean and reserved characters. Browser login affects account selection; verify actual sender.
- Missing required files prevent a ready-to-submit result. Upload all applicable required documents and useful selected supporting files automatically when access is available, without asking again for already authorized uploads. Exclude unrelated or disallowed material.
- A link cannot guarantee attachments, and an unsent draft is not a sent message. A user's report of sending does not prove the recipient accepted an application.
