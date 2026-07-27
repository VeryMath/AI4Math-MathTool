# AI4Math-MathTool

AI4Math-MathTool is the VeryMath repository for standalone mathematical tools
with stable data contracts, executable helpers, and independently testable
runtime behavior.

## Included tools

| Tool | Purpose | Status |
| --- | --- | --- |
| [`math-glossary`](skills/math-glossary/) | Build, review, back up, import, export, and maintain bilingual mathematical glossaries | Local course-edition candidate; publication blocked pending contributor authorization and license |

Each package keeps its own workflow, dependencies, provenance, normalization
record, and tests. Course origin is recorded as metadata; it does not determine
repository boundaries.

## Validation

```bash
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s skills/math-glossary/tests -v
```

## Publication status

This checkout is an unpublished review candidate. The original submission is
stored separately in a teacher-controlled archive and is ignored by Git.
No public repository or release should be created until the contributor's
publication authorization, attribution preference, repository license, and
third-party material review are recorded as confirmed.

See [LICENSE_STATUS.md](LICENSE_STATUS.md) for the current rights gate.
