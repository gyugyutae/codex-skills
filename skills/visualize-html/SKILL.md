---
name: visualize-html
description: Turn user-supplied notes and images into minimal, visual HTML presentation slides for a speaker to explain aloud. Use for requests such as 노션 메모를 그림 위주 발표 HTML로, 글은 적게 두 장으로, or 사진을 보고 설명할 자료. Prefer this over document-style layouts when the HTML is a visual aid rather than a standalone reading experience.
---

# Visual Talk HTML

Create a speaker's visual aid, not a scrolling report. The speaker carries the explanation; each screen exposes the main concepts and their relationships.

## Content boundary

- Read the supplied notes and inspect supplied images before choosing the layout. For Notion ZIPs, read Markdown and resolve its relative image paths.
- Use only supplied content unless the user requests expansion or research. Shorten sentences into faithful keywords; do not invent examples, code, benefits, technical claims, or sections to fill space.
- Preserve source topic order. User-requested emphasis can change visual prominence without changing the narrative order.
- Reuse requested original images without redrawing or replacing them. Do not assume a diagram's contents from its filename; inspect it when needed.
- If a source claim appears incorrect, raise a concise correction before changing its meaning. Do not present a faithful transcription as independently verified research.

## Layout decisions

- Use the requested slide count. For a brief two-topic request without a count, two screens is a reasonable default; do not impose two slides on larger requests.
- One main message per screen. Remove long paragraphs, lengthy code, decorative intros, reference pages, and unrelated context unless requested.
- Turn parallel concepts into large adjacent visual blocks. Each block gets a short heading, one simple diagram, and a one- or two-line caption. Make the concepts, not numbering or decoration, visually dominant.
- Draw simple source-grounded relationships with inline SVG: object/table, mapping pairs, arrows, interface/implementation connections. Do not add semantics that the source does not support.
- For an original architecture image, make the image the focal point and place only a few short role labels beside it. Check that text inside the source image remains legible.
- Use arrows only with a clear meaning (execution, code reference, transformation). Do not combine different arrow meanings into one ambiguous chain.
- Prefer a white background, one quiet accent color, generous spacing, and restrained borders. No hero banner, dashboard chrome, ornamental badges, or gradients by default.
- Do not shrink a report until it fits. Reduce visible text and strengthen visual grouping. If all source text must be retained, clarify the conflict with a sparse presentation or use speaker notes when authorized.

## HTML artifact

- Default to one self-contained local HTML file. Inline CSS, JS, and SVG; embed original images as base64 data URLs so downloading one file is sufficient. No CDN or external font requirement.
- Each slide fits the target desktop viewport without vertical scrolling, typically a 16:9 presentation screen. Maintain readable headings and captions at 1366×768 and 1440×900. Adapt narrow screens without clipping content.
- Provide only previous/next buttons and a page counter. Support left/right arrow keys. Optional fullscreen or print controls only when useful or requested.
- Keep inactive slides hidden and inaccessible to keyboard navigation; label controls and provide image alt text. If printing is supported, print every slide as a separate landscape page.
- Verify slide count, embedded assets, source fidelity, and navigation. Use browser inspection when available; do not claim visual verification if only static checks ran.
- Save to the user's selected location or a task-specific workspace folder. Upload or publish only within the user's authorized scope; an existing upload request may authorize replacing that same artifact. Preserve its file ID when updating.

## Example composition

For supplied notes about four EF Core settings plus clean architecture:

1. Settings screen: four equal visual blocks for entity, DbContext, mapping, and connection registration; a small scaffolding strip below if present in the notes.
2. Architecture screen: the original architecture picture large on the left, a few supplied role/interface keywords on the right, and a compact execution flow only if supplied.

This is a composition example, not mandatory content for unrelated topics.
