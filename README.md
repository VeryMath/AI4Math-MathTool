# AI4Math-MathTool

[中文说明](README.zh-CN.md)

AI4Math-MathTool is the VeryMath repository for standalone mathematical tools
and lightweight coding-agent adapters. Each package provides an explicit
workflow, provenance, and independently testable behavior.

## Included tools

| Tool | Purpose | Status |
| --- | --- | --- |
| [`math-glossary`](skills/math-glossary/) | Build, review, back up, import, export, and maintain bilingual mathematical glossaries | Released in [`v0.1.0`](https://github.com/VeryMath/AI4Math-MathTool/releases/tag/v0.1.0) under the MIT License |
| [`matlab-runner`](skills/matlab-runner/) | Route explicit MATLAB tasks through an available MATLAB MCP server with execution, testing, and numerical-validation evidence | Review candidate; unreleased |

Each package keeps its own workflow, dependencies, provenance, normalization
record, and tests. Course origin is recorded as metadata; it does not determine
repository boundaries.

## Validation

```bash
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s skills/math-glossary/tests -v
python3 -m unittest discover -s skills/matlab-runner/tests -v
```

## Publication status

This is the public canonical repository. The initial
[`v0.1.0`](https://github.com/VeryMath/AI4Math-MathTool/releases/tag/v0.1.0)
release is licensed under the [MIT License](LICENSE); the source-publication
instruction and third-party review are recorded in
[`skills/math-glossary/PROVENANCE.yaml`](skills/math-glossary/PROVENANCE.yaml).
The original submission remains in a teacher-controlled, Git-ignored archive.
Contributor names use the course-wide English romanization convention.

`matlab-runner` is a separate review candidate contributed by `njustar2002`.
Its publication authorization and source checksum are recorded in
[`skills/matlab-runner/PROVENANCE.yaml`](skills/matlab-runner/PROVENANCE.yaml).
It is not included in the historical `v0.1.0` release.

See [THIRD_PARTY.md](THIRD_PARTY.md) for dependency and material boundaries,
[SECURITY.md](SECURITY.md) for safe operation, and
[PUBLISHING.md](PUBLISHING.md) for the remote publication procedure.
