---
name: visualize-html
description: Use when the user wants notes, images, or their understanding from a conversation turned into minimal visual HTML slides for explaining aloud, such as 그림 위주 발표 HTML or 내가 이해한 내용으로 발표자료. Prefer this over a document layout for a speaker's visual aid.
---

# Visual Talk HTML

Create one self-contained HTML visual aid from what the user understands and considers important, with one main message per screen. The user owns the meaning; choose the visual presentation yourself.

## Select content and clarify meaning

- Read supplied notes and relevant conversation; inspect supplied images. For Notion ZIPs, resolve Markdown-relative image paths.
- Select user-provided notes, explicitly accepted explanations, and ideas the user restates in their own words or repeatedly emphasizes. Treat those restatements as understood and important without requiring another confirmation. An unanswered assistant suggestion is not accepted content.
- Before generating, ask about ambiguity that changes meaning, relationships, or which core content belongs. Ask a focused question and wait for the answer before rendering the affected content. Do not guess a relationship or add an "unknown" annotation as a substitute for clarification. Choose layout, colors, shapes, wording compression, and visual hierarchy without asking.
- Preserve source topic order and requested emphasis. Faithful shortening, heading cleanup, and visual regrouping are allowed. New examples, claims, benefits, numbers, causal links, and connecting arrows need supplied support or an explicit expansion/research request.
- If a source claim appears incorrect, explain the correction briefly in chat before changing its meaning. Do not present user understanding as independently verified research.
- Reuse requested original images without redrawing or replacing them. Do not assume a diagram's contents from its filename; inspect it when needed.

## Compose each screen

- Default composition: **short concept title → meaningful diagram → one- or two-line core caption**. Put parallel concepts side by side. If a picture adds no explanatory value, use concise keywords or a comparison instead of decoration.
- Use the requested count or maximum. A brief two-topic request can use two screens; do not impose two screens on larger requests.
- Draw source-grounded relationships with inline SVG; use [diagram guidance](references/diagrams.md) for changes, connections, and comparisons. Make original architecture images the focal point with only essential labels; keep their text legible.
- Use a white background, one quiet accent color, generous spacing, and restrained borders. Omit decorative intros, dashboard chrome, ornamental badges, gradients, long paragraphs, lengthy code, and extra reference pages by default.
- Slide content consists of the core title, visual, and explanatory caption. Do not append bottom footers with progress, verification status, caveats, future work, or author commentary (for example, "not yet executed"). Report material limitations in chat, outside the artifact. If the user explicitly requests such a statement as presentation content, include it in the requested context rather than an automatic footer. Previous/next controls and the page counter are separate navigation.
- Reduce repetition before reducing text size. Preserve emphasized ideas; if the requested count cannot contain the required content readably, clarify the conflict. Add speaker notes only when authorized.

## Build, verify, and deliver

- Inline CSS, JS, and SVG; embed original images as base64 data URLs. No CDN or external font requirement.
- Fit each slide to the desktop viewport without vertical scrolling, typically 16:9. Keep headings and captions readable at 1366×768 and 1440×900; adapt narrow screens without clipping.
- Provide only previous/next buttons and a page counter. Support left/right arrow keys. Optional fullscreen or print controls only when useful or requested.
- Keep inactive slides hidden and inaccessible to keyboard navigation; label controls and provide image alt text. If printing is supported, print every slide as a separate landscape page.
- Verify content selection, source-grounded relationships, slide count, embedded assets, navigation, and absence of unsolicited footer commentary. Inspect diagrams for consistent identities and meaningful arrows. Use browser inspection when available; do not claim visual verification from static checks alone.
- Save to the user's selected location or a task-specific workspace folder. Upload or publish only within the user's authorized scope; an existing upload request may authorize replacing that same artifact. Preserve its file ID when updating.
