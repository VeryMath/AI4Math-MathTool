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
- Preserve the repository's MIT license and keep third-party license boundaries
  documented in `THIRD_PARTY.md`.

## Validation

Run:

```bash
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s skills/math-glossary/tests -v
python3 -m unittest discover -s skills/matlab-runner/tests -v
```

Package-level tests must use temporary directories and must not mutate source
fixtures, a user's glossary, MATLAB files, or a shared MATLAB session. Static
`matlab-runner` tests do not establish that MATLAB executed successfully.
