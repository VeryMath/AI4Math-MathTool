# Repository Guidelines

## Scope

This repository hosts standalone mathematical tools with explicit input/output
contracts and runnable implementations. Keep every tool isolated under
`skills/<package-name>/`.

## Package rules

- Keep `SKILL.md` as the canonical agent workflow.
- Put executable helpers in `scripts/` and supporting documentation in
  `references/`.
- Record source lineage in `PROVENANCE.yaml` and all release-only edits in
  `NORMALIZATION.md`.
- Do not publish original course archives, private intake records, credentials,
  local absolute paths, or unreviewed third-party data.
- Do not add a repository license until the rights holder has approved it.

## Validation

Run:

```bash
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s skills/math-glossary/tests -v
```

Package-level tests must use temporary directories and must not mutate source
fixtures or a user's glossary.
