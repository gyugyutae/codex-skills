# Skill authoring conventions

When creating or revising a skill here, start from `template/SKILL.md`
and read `spec/authoring-guide.md`. Preserve existing behavior and authorization
boundaries when shortening instructions. Delete unnecessary template sections.
Do not modify bundled system skills to enforce these conventions.

Repository layout and optional skill resources are documented in `spec/skill-structure.md`.
Keep runtime resources self-contained under each skill; development tests live under `tests/`.
