# Codex Skills

개인 작업에 사용하는 Codex 스킬 모음입니다.

| 스킬 | 설명 |
| --- | --- |
| [visual-talk-html](skills/visual-talk-html/SKILL.md) | 메모와 원본 이미지를 글이 적고 그림이 중심인 HTML 발표 자료로 정리합니다. |
| [hwp-form-authoring](skills/hwp-form-authoring/SKILL.md) | 기존 한글 양식을 유지해 개인정보·증빙·서명을 채우고 HWP·PDF를 검증합니다. 개인 자료가 포함된 비공개 스킬입니다. |
| [exam-study-notes](skills/exam-study-notes/SKILL.md) | 제공한 자료·질문만으로 필수 내용을 보존한 최소 분량의 인쇄용 시험 정리 PDF를 만듭니다. |

## 설치

저장소를 내려받은 후 사용할 스킬 폴더를 `~/.codex/skills/`에 복사합니다.

```bash
cp -R skills/visual-talk-html ~/.codex/skills/
```

## 사용 예시

```text
$visual-talk-html 이 노션 메모로 발표용 HTML 만들어줘.
원문 순서를 유지하고, 추가 내용 없이 그림과 핵심 단어 위주로 두 장 구성해줘.
```

각 스킬의 상세 지침은 해당 폴더의 `SKILL.md`에서 확인할 수 있습니다.

## 스킬 작성 템플릿

새 스킬 작성·기존 스킬 수정은 [AGENTS.md](AGENTS.md)의 지침에 따라
[공통 템플릿](templates/SKILL.template.md)과 [짧은 실행 안내 원칙](templates/authoring-guide.md)을 적용합니다.
본문은 작업 선택·직접 실행·결과 검증 중심으로 쓰고, 상세 내용은 참고문서로 분리합니다.
단순한 스킬에는 불필요한 템플릿 항목을 제거합니다.

다른 작업 폴더에서도 적용하려면 `templates/SKILL.template.md`와 `authoring-guide.md`를
`~/.codex/skill-templates/`에 복사하고, [전역 지침 조각](templates/AGENTS.fragment.md)을
기존 `~/.codex/AGENTS.md`에 추가합니다. 기존 지침을 덮어쓰지 마세요.
GitHub 설치만으로 전역 지침까지 자동 변경되지는 않습니다.

서명 검증 회귀 테스트:

```bash
python3 -m unittest discover -s skills/hwp-form-authoring/tests -v
```

테스트에는 PyMuPDF와 Pillow가 필요하며 개인 문서를 테스트 데이터로 사용하지 않습니다.
