# Skill repository structure

Use the self-contained Agent Skills layout shared with Anthropic's examples.
Only SKILL.md is required; add resources when the skill needs them.

```text
codex-skills/
├── AGENTS.md                    # Codex repository guidance
├── CLAUDE.md                    # Claude Code imports the same guidance
├── README.md
├── template/SKILL.md            # Starting point for a new skill
├── spec/                        # Repository-wide authoring guidance
├── tests/<skill-name>/          # Development tests, not runtime assets
└── skills/<skill-name>/
    ├── SKILL.md                 # Short task selection, execution, verification
    ├── scripts/                 # Optional executable helpers
    ├── references/              # Optional on-demand instructions
    ├── assets/                  # Optional output/input resources
    └── agents/openai.yaml       # Optional Codex UI metadata
```

`assets/`, `references/` and `scripts/` are also used by Anthropic's skill-creator;
they are not Codex-only directories. `agents/openai.yaml` is kept for Codex labels
and default prompts; other Agent Skills consumers can ignore it. Do not confuse
it with Claude subagent definitions. Do not create all optional folders for every skill.

Keep references, images and runtime scripts inside the skill so installing one
folder remains sufficient. Do not move private profile/signature assets into a
public shared directory. Developer tests can reference repository skill code;
they are not required for using an installed skill.

Sources:
- https://github.com/anthropics/skills
- https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md
- https://agentskills.io/specification

The repository is still private. This layout does not install a Claude plugin or
change signature/submission permissions.
