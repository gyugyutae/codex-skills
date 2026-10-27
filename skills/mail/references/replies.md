# Existing conversations and attached reply drafts

## Find the conversation

Treat “reply”, “회신”, “답장”, and clear continuation of an ongoing exchange as a reply request. Discover the live Gmail profile, search, read-thread, create/update-draft and draft-reading schemas. Verify the authenticated mailbox against the intended sender account before creating a draft; use the correct account's authenticated webmail if necessary. Do not change From to impersonate a different mailbox.

Search by the known correspondent address plus subject, topic and date clues from the conversation. Read the matching thread, including the latest messages, before choosing the reply target. Prefer the latest relevant incoming message, respecting Reply-To; do not simply reply to the newest message from that person on an unrelated topic. Multiple materially plausible threads, an unclear sender account, or an unavailable required file justify a concise question. If one thread clearly matches, proceed without confirmation. Default to replying to the correspondent; use Reply All when requested or clearly required by the conversation, excluding the user's own addresses.

## Create a real reply

Keep the existing subject with the normal Re: prefix. With the current Gmail create_draft tool, set `reply_message_id` to the fetched Gmail message ID of the chosen incoming message; this is not the RFC Message-ID header or a thread ID. Check the current schema rather than assuming it remains unchanged. A Re: subject alone does not establish a reply. In webmail, open the verified message and use Reply or Reply All.

The local helper accepts optional `reply_message_id` in draft mode and adds it to `draftArgs`; compose mode deliberately rejects it because a generic compose URL cannot guarantee a threaded reply. Conversation/thread identifiers used for verification should come from actual read results.

Read [attachments.md](attachments.md) for selecting and uploading prompt files or previously discussed documents. Use the relevant final files automatically when their identity and purpose are established. A statement that a certificate was issued establishes a need for the document, not access to its bytes: locate it or request the missing file rather than inventing an attachment. Attach the selected files to the actual reply MIME tree. Do not reattach old or unrelated sensitive documents by default.

Reuse the matching existing draft on retries. When update_draft replaces `payload`, include all intended attachments because replacement drops omitted parts. Do not repeatedly create duplicate drafts after uncertain tool results; inspect existing drafts first.

## Verify and return

Re-read the draft/message and verify sender, recipients, body, subject, reply context/thread linkage and attachment names/count/size against the manifest. Do not claim threading or attachment verification beyond the fields/UI actually available. Return an observed draft URL, or the verified conversation URL and clear instructions for opening the prepared reply if no draft-specific URL is available. Never invent a URL from an opaque draft ID.

If the intended account cannot be accessed, explain that limitation and return the reply text, accessible source files, and a verified conversation link if available. Do not silently turn a requested reply into a new email, or claim files are attached when only a link/MIME payload was prepared. Change “attached” wording when no uploaded attachment exists.

Fill the intended recipient even during a requested attachment test unless the user explicitly asks for a recipient-free test. Testing does not authorize changing the sender account: use a different authenticated account only when that test scope is established with the user.

Prefer an observed direct draft-editor link and verify that it opens the intended draft when browser access is available. A verified Gmail message ID can identify the conversation, but do not claim a constructed conversation URL opens the editor unless tested. If only a conversation or Drafts-folder link is available, label it accurately and state what remains unverified.

Default to an unsent reply draft. A request to write/reply authorizes preparation and relevant attachments; send only when the user explicitly requests actual sending.

## Behavioral checks

- One clear Alyx funding thread plus an uploaded final bank certificate: choose that thread, upload only the relevant certificate, and prepare an unsent reply with the original subject.
- Same correspondent, unrelated admissions and funding threads: use the user's topic to resolve; ask only if both remain plausible.
- GNU sender requested but only personal Gmail authenticated: use authenticated GNU webmail if available; otherwise report missing account access, without creating a personal-account draft.
- Certificate mentioned but absent: search authorized sources, then request the file if unavailable; do not claim it is attached.
- Failed upload or uncertain create response: inspect/reuse drafts, repair or report incomplete status; never present a generic compose link as a verified attached reply.
