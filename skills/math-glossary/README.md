# math-glossary

`math-glossary` builds and maintains a bilingual mathematical glossary whose
JSON file is the source of truth. It supports backup, Excel import/export,
optional AI-assisted example enrichment, and an optional local Flask management
interface.

This package preserves the student's course workflow as an independent skill.
The course edition only normalizes the package layout, portability, safety,
configuration, documentation, and tests. It does not merge or inherit another
VeryMath skill.

## Capabilities

- Parse or guide extraction from PDF, text, Markdown, Excel, JSON, CSV, YAML,
  MDX, and OCR-derived sources.
- Build `glossary.json` directly from CSV/TSV/JSON/YAML with source-location
  tracing.
- Sort, number, merge, and maintain glossary entries under the schema in
  [`references/glossary-schema.md`](references/glossary-schema.md) and
  [`references/glossary.schema.json`](references/glossary.schema.json).
- Back up `glossary.json` and round-trip glossary entries through Excel.
- Run a local Web UI for search and CRUD operations.
- Optionally enrich missing examples through an explicitly configured
  OpenAI-compatible endpoint.

## Install

Core offline helpers:

```bash
python3 -m pip install -r requirements.txt
```

Optional AI-assisted enrichment:

```bash
python3 -m pip install -r requirements-ai.txt
```

Review dependency installation with the user before installing packages.
`mdict-utils` is optional and needed only for MDX extraction.
The Web UI has no authentication and should remain bound to its default
loopback address.

## Quick smoke test

```bash
python3 -m unittest discover -s tests -v
```

Build from structured data:

```bash
python3 scripts/glossary_build.py /path/to/terms.csv
```

The default output is `/path/to/术语库/glossary.json`. Existing JSON is never
overwritten unless `--force` is explicit. If Excel dependencies are unavailable,
the command reports “JSON complete, Excel pending” and exits with status 3.

Export an existing glossary:

```bash
python3 scripts/glossary_export.py export /path/to/glossary.json /path/to/output
```

Start the local Web UI without opening a browser:

```bash
python3 scripts/glossary_web.py \
  --glossary /path/to/glossary.json \
  --no-browser
```

See [`README.zh-CN.md`](README.zh-CN.md), [`SKILL.md`](SKILL.md), and
[`NORMALIZATION.md`](NORMALIZATION.md) for the complete workflow and change
boundary.

## Publication status

This is an MIT-licensed local release candidate, ready for remote publication.
The publication instruction, normalization approval, and third-party review
are recorded in [`PROVENANCE.yaml`](PROVENANCE.yaml). It is not described as a
public release until the remote repository, passing CI run, and release tag
exist. The public contributor name is standardized as **Yunfeng Lu** under the
course-wide English-name policy.
