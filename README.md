# Personal Agent Skills

개인 작업용 스킬 모음입니다. Anthropic 예제와 같은 **스킬별 독립 폴더 + 필요한 자원만 포함**하는 구조를 따르며 Codex에서 사용합니다.

| 스킬 | 용도 |
| --- | --- |
| [visual-talk-html](skills/visual-talk-html/SKILL.md) | 원본 메모·이미지로 글이 적고 그림이 중심인 HTML 발표 자료 작성 |
| [hwp-form-authoring](skills/hwp-form-authoring/SKILL.md) | 원본 한글 양식, 날짜·체크·자필 공란, 증빙 및 HWP/PDF 검증 |
| [exam-study-notes](skills/exam-study-notes/SKILL.md) | 제공 자료 범위를 지키는 간결한 인쇄용 시험 정리 PDF 작성 |
| [application-mail](skills/application-mail/SKILL.md) | 채팅에서 바로 여는 GNU 메일 링크, 올바른 계정의 필수·추천 서류 첨부 초안 준비 |

HWP 스킬에는 개인 프로필·서명이 포함되어 있어 이 저장소는 비공개로 유지합니다.

## 구조

```text
.
├── AGENTS.md / CLAUDE.md        # 같은 저장소 작성 지침
├── template/SKILL.md            # 새 스킬 시작점
├── spec/                       # 작성 원칙과 구조 설명
├── tests/<skill-name>/         # 개발용 테스트
└── skills/<skill-name>/
    ├── SKILL.md
    ├── scripts/                # 필요할 때만
    ├── references/             # 필요할 때만
    ├── assets/                 # 필요할 때만
    └── agents/openai.yaml      # Codex용 선택 메타데이터
```

Anthropic도 `scripts/`, `references/`, `assets/`를 사용합니다. 폴더를 없애기보다 역할을 분리했습니다.
Codex의 표시 이름·기본 프롬프트를 보존하려고 `agents/openai.yaml`은 유지합니다.
자세한 기준: [구조 설명](spec/skill-structure.md).

## 설치와 사용

Codex에서 다음처럼 요청합니다. 비공개 저장소에 접근할 GitHub 인증이 필요합니다.

```text
$skill-installer https://github.com/gyugyutae/codex-skills/tree/main/skills/hwp-form-authoring 이 스킬을 설치해줘.
```

수동 설치 시 기존 설치본을 먼저 확인하고, 해당 스킬 폴더 전체를 런타임의 사용자 스킬 경로에 복사합니다.
현재 개인 환경은 `~/.codex/skills/`를 사용하며 사용자 공통 경로로 `~/.agents/skills/`도 쓰입니다.
GitHub 수정은 기존 설치본에 자동 동기화되지 않습니다.

```text
$hwp-form-authoring 이 신청서의 원본 서식을 유지해 채워줘. 자필서명란은 비워줘.
```

## 새 스킬 작성

[템플릿](template/SKILL.md) → [작성 원칙](spec/authoring-guide.md) → 실제 결과 검증 순서로 진행합니다.
본문은 짧은 작업 선택·실행·검증 안내로 쓰고, 세부 규칙은 필요한 참고문서에 둡니다.

다른 작업 폴더에서도 같은 원칙을 사용하려면 다음 두 파일을 복사합니다.

```bash
mkdir -p ~/.codex/skill-templates
cp template/SKILL.md ~/.codex/skill-templates/SKILL.template.md
cp spec/authoring-guide.md ~/.codex/skill-templates/authoring-guide.md
```

[전역 지침 조각](spec/AGENTS.fragment.md)은 기존 `~/.codex/AGENTS.md`에 추가합니다.
기존 파일을 덮어쓰지 마세요. 스킬 설치만으로 전역 지침이 자동 변경되지는 않습니다.

## 검증

```bash
python3 -m unittest discover -s tests/hwp-form-authoring -v
```

서명 검증 테스트는 PyMuPDF와 Pillow를 사용합니다. 개인 문서 없이 합성 PDF로 검사합니다.
개별 스킬 실행 도구는 해당 `SKILL.md`를 참고하세요.
