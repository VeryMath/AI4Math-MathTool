# AI4Math-MathTool

AI4Math-MathTool is the VeryMath repository for standalone mathematical tools
with stable data contracts, executable helpers, and independently testable
runtime behavior.

## Included tools

| Tool | Purpose | Status |
| --- | --- | --- |
| [`math-glossary`](skills/math-glossary/) | Build, review, back up, import, export, and maintain bilingual mathematical glossaries | MIT-licensed local release candidate; ready for remote publication |

Each package keeps its own workflow, dependencies, provenance, normalization
record, and tests. Course origin is recorded as metadata; it does not determine
repository boundaries.

## Validation

```bash
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s skills/math-glossary/tests -v
```

## Publication status

This checkout is a tested, unpublished release candidate. It is licensed under
the [MIT License](LICENSE); the source-publication instruction and third-party
review are recorded in
[`skills/math-glossary/PROVENANCE.yaml`](skills/math-glossary/PROVENANCE.yaml).
The original submission remains in a teacher-controlled, Git-ignored archive.
Contributor names use the course-wide English romanization convention.

See [THIRD_PARTY.md](THIRD_PARTY.md) for dependency and material boundaries,
[SECURITY.md](SECURITY.md) for safe operation, and
[PUBLISHING.md](PUBLISHING.md) for the remote publication procedure.
