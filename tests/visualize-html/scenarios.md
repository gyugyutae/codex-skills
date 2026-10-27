# Content selection and visual meaning regression scenarios

Run scenarios with a fresh context and the skill. Keep generated artifacts in a temporary folder, not in the runtime skill. Review rendered content and SVG meaning; metadata validation alone is insufficient.

## 1. Accepted notes versus work status and unanswered suggestions

Request:

> 두 장 발표 HTML로 정리해줘. 내가 이해한 건 문서에 원본 기록을 남기고 주간회의에서 함께 검토한다는 거야. 이 두 가지가 중요해. 이전에 AI는 자동 알림, AI 요약, 대시보드도 제안했지만 나는 아직 답하지 않았어. 일정은 아직 미정이고 실행 검증은 안 했다는 작업 메모도 있어. 레이아웃은 알아서 해줘.

Expected: two screens about original records and weekly review, with core captions. No status footer or unsolicited capabilities, including a list of excluded suggestions. No layout clarification needed. Navigation remains available.

Observed baseline with the previous skill: slide 1 appended “작업 메모 · 일정 미정 · 실행 검증 전”; slide 2 appended “응답 전인 AI 제안 · 자동 알림 · AI 요약 · 대시보드”. Both are off-scope slide content.

## 2. Meaning is missing

Request:

> A팀과 B팀이 있고 결과를 모은다. 두 팀이 동시에 진행하는지, A 결과가 B 입력인지는 아직 모르겠어. 한 장으로 그려줘.

Expected: ask a focused content question and wait before drawing that relationship. Do not choose sequential/parallel semantics or substitute an unknown-status note for clarification.

Observed baseline: proposed drawing the teams with a “미정” annotation rather than asking first. It avoided inventing an edge but did not resolve the meaning.

## 3. Restatement and emphasis count as understanding

Conversation fixture:

> Assistant: One possibility is automatic scoring; another is manual comparison.
> User: 그러니까 같은 기준으로 비교하고 차이를 내가 설명하는 거네. 같은 기준으로 보는 게 제일 중요해. 이 내용으로 한 장 만들어줘. 색이나 배치는 알아서 해.

Expected: include a common comparison criterion and explaining differences, without demanding “I understand” or introducing automatic scoring. Choose the visual arrangement independently.

## 4. Before/after identity and user-requested content

Request:

> 두 문서에 같은 안내가 있다. 공통 안내를 별도 문서 하나로 합치고 원래 두 문서는 그 안내를 참조한다. 한 장으로 변경 전후를 그려줘. “아직 검토 전”이라는 문구는 내가 설명할 핵심이니까 제목 아래에 꼭 넣어줘.

Expected: preserve the identity of the guidance. Before: duplicated content. After: one shared copy and two referring documents; do not leave duplicate content in the old documents. Transformation and reference arrows remain distinguishable. Include the explicitly requested statement under the title, without appending a generic footer.

## Forward-check results

The revised skill was exercised in fresh agent contexts against scenarios 1–4. Generated HTML and the clarification response were read directly:

- Scenario 1: both screens contain only original records and weekly review; work-status and unanswered suggestions are absent. Title/diagram/core-caption composition and navigation are present.
- Scenario 2: asks whether the teams work independently or sequentially and waits; it does not generate the ambiguous diagram.
- Scenario 3: includes shared criteria and explaining differences, omits automatic scoring, and chooses the layout without asking.
- Scenario 4: before/after SVG removes old duplicate content, retains the two source documents as users of the shared guide, and distinguishes transformation/reference arrows. The explicitly requested statement appears directly below the title.

These are bounded regression examples, not a statistical guarantee of future generation behavior.

Browser spot checks: scenario 1's first screen and scenario 4's single screen were rendered in Edge and visually inspected. The core captions are retained; no unsolicited status footer appears. The explicitly requested scenario 4 statement remains below the title, and its before/after contents and reference arrows are legible.

## Preserved behavior checks

- Requested original images remain intact and embedded; no invented redraw.
- Explicit slide count/maximum, source order, keyboard navigation, and hidden inactive slides remain supported.
- Publishing still requires existing task authorization; changing this skill does not grant future upload permission.
